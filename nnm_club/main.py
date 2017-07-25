# -*- coding: utf8 -*-
import traceback

from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider
from bs4 import BeautifulSoup
from datetime import datetime

import re


log = CPLog(__name__)


class nnm_club(TorrentProvider, MovieProvider):

    baseurl = 'https://nnm-club.name/forum/'
    urls = {
        'test' : 'https://nnm-club.name',
        'login' : baseurl + 'login.php',
        'login_check': baseurl + 'contact.php',
        'detail' : baseurl + 'viewtopic.php?t=%s',
        'search' : baseurl + 'tracker.php?nm=%s&o=7&c=14',
        'download' : baseurl + 'download.php?id=%s',
    }

    http_time_between_calls = 1 #seconds
    cat_backup_id = None

    def _searchOnTitle(self, title, movie, quality, results):
        if len(title) == 0:
            log.debug('Skipping. Reason: Title is empty')
            return
            
        log.debug('Searching nnm_club for %s' % (title))

        if len(title) <= 3:
            log.debug('Skipping. Reason: Title is too short for search')
            return

        url = self.urls['search'] % title.replace(':', ' ')
        data = self.getHTMLData(url).decode('cp1251')

        log.debug('Received data from nnm_club')
        if data:
            log.debug('Data is valid from nnm_club')
            html = BeautifulSoup(data)

            try:
                result_table = html.find('table', attrs = {'class' : 'forumline tablesorter'})
                if not result_table:
                    log.debug('No table results from nnm_club')
                    return

                table_head = result_table.find('thead')
                header_cells = table_head.find_all('th')

                # Cells idx
                title_cell_idx = header_cells.index(table_head.find('th', title=u'Тема'))
                dl_idx = header_cells.index(table_head.find('th', title=u'Скачать .torrent'))
                size_idx = header_cells.index(table_head.find('th', title=u'Размер'))
                seed_idx = header_cells.index(table_head.find('th', title='Seeders'))
                leech_idx = header_cells.index(table_head.find('th', title='Leechers'))
                date_added_idx = header_cells.index(table_head.find('th', title=u'Добавлено'))

                torrents = result_table.find_all('tr', attrs = {'class' : re.compile("^prow")})
                for result in torrents:
                    all_cells = result.find_all('td')

                    # Cells
                    copyright_cell = all_cells[title_cell_idx].find('img', title=u'Копирайт')
                    if not copyright_cell:
                        copyright_cell = all_cells[dl_idx].find('span')

                    title_cell = all_cells[title_cell_idx].find('a')
                    if not copyright_cell:
                        dl_cell = all_cells[dl_idx].find('a')
                    size_cell = all_cells[size_idx]
                    seed_cell = all_cells[seed_idx]
                    leech_cell = all_cells[leech_idx]
                    date_added_cell = all_cells[date_added_idx]

                    # Torrent data
                    topic_id = title_cell['href']
                    topic_id = topic_id.replace('viewtopic.php?t=', '')
                    if not copyright_cell:
                        torrent_id = dl_cell['href']
                        torrent_id = torrent_id.replace('download.php?id=', '')

                    torrent_name = self.formatTitle(title_cell.getText())
                    torrent_size = self.parseSize(size_cell.contents[1].replace(',', '.').strip())
                    torrent_seeders = tryInt(seed_cell.getText())
                    torrent_leechers = tryInt(leech_cell.getText())
                    torrent_age = self.calculateAge(date_added_cell.contents[1].strip())
                    torrent_detail_url = self.urls['detail'] % topic_id
                    if not copyright_cell:
                        torrent_url = self.urls['download'] % torrent_id

                    log.debug('Title: %s' % torrent_name)
                    log.debug('Size: %s' % torrent_size)
                    log.debug('Forum: %s' % torrent_detail_url)
                    if not copyright_cell:
                        log.debug('Dl: %s' % torrent_url)
                    log.debug('Seed: %d' % torrent_seeders)
                    log.debug('Leech: %d' % torrent_leechers)
                    log.debug('Age: %s' % torrent_age)
                    
                    if copyright_cell:
                        log.debug('Skipping. Reason: This release is unavailable due copyright (use non-russian proxy to bypass)')
                        continue
                    
                    results.append({
                        'id': torrent_id,
                        'name': torrent_name,
                        'size': torrent_size,
                        'seeders': torrent_seeders,
                        'leechers': torrent_leechers,
                        'url': torrent_url,
                        'detail_url': torrent_detail_url,
                        'age': torrent_age,
                    })

            except:
                log.error('Failed to parse nnm_club: %s' % (traceback.format_exc()))

    def getLoginParams(self):
        log.debug('Getting login params for nnm_club')
        return {
            'username': self.conf('username'),
            'password': self.conf('password'),
            'login': '%C2%F5%EE%E4',
            'autologin': 'on',
        }

    def loginSuccess(self, output):
        isLoginSuccessful = 'login.php?logout=true' in output.lower()
        log.debug('Checking login success for nnm_club: %s' % isLoginSuccessful)
        return isLoginSuccessful

    loginCheckSuccess = loginSuccess
    
    # Input format: Translated Title / Original Title (year) rest/of[the]name
    # Output format: Original.Title.(year).[resolution].rest.of.the.name
    def formatTitle(self, raw_title):
        log.debug('Raw Title: %s' % raw_title)

        # Workaround for filtering 1080p and 720p by CouchPotato: BDRip is a source, not a video quality!
        title = raw_title.replace('BDRip', '')

        # Year search (should be always in '(' ')' )
        p = re.compile('\([0-9]{4}\)')
        m = p.search(title)
        if not m:
            # Can't format properly without a year anyway
            return title

        year = m.group()

        title_split = title.split(year)
                  
        # Keep only last title name (nnm uses '/' to delimit title names in different languages)
        title_only = title_split[0].split('/')[-1].strip()
        title_only = re.sub('[ \:]', '.', title_only)
        
        rest = re.sub('[^0-9a-zA-Z]+', '.', title_split[1])

        # Resolution (1080p, 720p and etc)
        p = re.compile('\.[0-9]{3,4}[pi](\.)?')
        m = p.search(rest)
        resolution = ''
        if m:
            resolution = m.group().replace('.','')
            rest = rest.replace(resolution, '')
            resolution = '[' + resolution + ']'
            
        title = title_only + '.' + year + '.' + resolution + '.' + rest

        title = re.sub('\.\.+', '.', title)
        title = re.sub('(^\.)|(\.$)', '', title)
        
        return title
    
    def calculateAge(self, date_str):
        return (datetime.today() - datetime.strptime(date_str, '%d-%m-%Y')).days
