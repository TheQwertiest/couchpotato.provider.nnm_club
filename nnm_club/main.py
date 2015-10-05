# -*- coding: cp1251 -*-
import traceback

from bs4 import BeautifulSoup
from couchpotato.core.helpers.encoding import tryUrlencode
from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider

import re


log = CPLog(__name__)


class nnm_club(TorrentProvider, MovieProvider):

    baseurl = 'https://nnm-club.me/forum/'
    urls = {
        'test' : 'https://nnm-club.me',
        'login' : baseurl + 'login.php',
        'login_check': baseurl + 'contact.php',
        'detail' : baseurl + 'viewtopic.php?t=%s',
        'search' : baseurl + 'tracker.php?nm=%s&o=7&c=14',
        'download' : baseurl + 'download.php?id=%s',
    }

    http_time_between_calls = 1 #seconds
    cat_backup_id = None

    def _searchOnTitle(self, title, movie, quality, results):

        log.debug('Searching nnm_club for %s' % (title))

        url = self.urls['search'] % (title.replace(':', ' '))
        data = self.getHTMLData(url)

        log.debug('Received data from nnm_club')
        if data:
            log.debug('Data is valid from nnm_club')
            html = BeautifulSoup(data)

            try:
                result_table = html.find('table', attrs = {'class' : 'forumline tablesorter'})
                if not result_table:
                    log.debug('No table results from nnm_club')
                    return

                torrents = result_table.find_all('tr', attrs = {'class' : re.compile("^prow")})
                for result in torrents:
                    all_cells = result.find_all('td')

                    title_cell = all_cells[2].find('a')
                    dl_cell = all_cells[4].find('a')
                    size_cell = all_cells[5]
                    seed_cell = all_cells[7]
                    
                    topic_id = title_cell['href']
                    topic_id = topic_id.replace('viewtopic.php?t=', '')

                    torrent_id = dl_cell['href']
                    torrent_id = torrent_id.replace('download.php?id=', '')
                    
                    size_txt_to_remove = size_cell.u.string
                    size = size_cell.getText("", strip=True).replace(size_txt_to_remove, '')
                    size = size.replace(',', '.')

                    torrent_name = title_cell.getText()
                    torrent_size = self.parseSize( size )
                    torrent_seeders = tryInt(seed_cell.getText())
                    torrent_detail_url = self.urls['detail'] % topic_id
                    torrent_url = self.urls['download'] % torrent_id

                    log.debug('Title? %s' % (torrent_name))
                    log.debug('Size %s?' % (torrent_size))   
                    log.debug('Forum %s?' % (torrent_detail_url))
                    log.debug('Dl %s?' % (torrent_url))
                    log.debug('seed %d?' % (torrent_seeders))
                    
                    results.append({
                        'id': torrent_id,
                        'name': torrent_name,
                        'size': torrent_size,
                        'seeders': torrent_seeders,
                        'url': torrent_url,
                        'detail_url': torrent_detail_url,
                    })
                    

            except:
                log.error('Failed to parse nnm_club: %s' % (traceback.format_exc()))

    def getLoginParams(self):
        log.debug('Getting login params for nnm_club')
        return {
            'username': self.conf('username'),
            'password': self.conf('password'),
            'autologin': 'checked',
            'login': '%C2%F5%EE%E4',
        }

    def loginSuccess(self, output):
        log.debug('Login output %s', output)        
        log.debug('Checking login success for nnm_club: %s' % ('True' if ('contact.php' in output.lower()) else 'False'))
        return 'contact.php' in output.lower()

    loginCheckSuccess = loginSuccess
