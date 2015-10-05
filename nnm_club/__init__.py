from .main import nnm_club

def autoload():
  return nnm_club()

config = [{
  'name': 'nnm_club',
  'groups': [
    {
      'tab': 'searcher',
      'list': 'torrent_providers',
      'name': 'NnmClub',
      'description': '<a href="https://nnm-club.me">NnmClub</a>',
      'wizard': True,
      'icon': 'AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaQicAXRQFADICAQAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADz4QA8PizAPu3XQDpjEIBtgkCABoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAIAEuyUAP3/8AD//akA//+hAP92SgCVAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFAAAAAAAAAAAAAAAAAEAADjLiQD8//wA//7RFP//+lX/WlsPlwAAAAMAAAAGAAAAAAAAAAAAAAAAEAgAQqNBAP99HADfIAYAfgAAABQAAAAX21UC///4AP///Sj/+/Z//lZcMJOOjQCrqIEAwQ4CADAAAAAAAAAAAGEXAM39oAD//7oA/9ucAP94GwDFVRkK6p0wAP//owD/+KoB/+FTC///uQD//+wA//67AP6QUQC9DggAGAAAAACPNQDl964A//qqAv//3AD//8sB/39WAP85AwX/nxkA/5MQAP/sJQD/0T8A//Z9AP/6kwD/86AA/qJGALwTAABEtzcA5cshAP/jOAD//7wg///+Dv/RUQH/AgEE8hcAAG40BgB3RAAAzlYCAPh0BAD/zh8A//+RAP//hQD/5B8A/xcAAEx+HgDXz5oc/8yfPv//2g7/6VMA/AkEABQAAAAAAAAAAQAAAA4cCgBBOwkAg3EfAKyPfQDEdkAAq0ELAGYAAAAABQMBQNldFf3/8w3///sA/7AoAPIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAchNAPLaLgD/+8AA//eOAP9qDAGpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFwLgCX0h8A//WiAP/+TQD/KgQAZAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALQwAZqgRAPr0hwD/2VIA/QAAAAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAoBACp6BAD/7H0A/3ZlALoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARAQAx4zcA/93AAPQAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACgEASawXAPMTCgAnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/D+sQfgfrEH4H6xBuAesQQADrEEAAaxBAACsQQAArEEBAKxBg/+sQQP/rEED/6xBg/+sQYf/rEGH/6xBj/+sQQ==',
      'options': [
        {
          'name': 'enabled',
          'type': 'enabler',
          'default': False,
        },
        {
          'name': 'username',
          'default': '',
        },
        {
          'name': 'password',
          'default': '',
          'type': 'password',
        },
        {
          'name': 'seed_ratio',
          'label': 'Seed ratio',
          'type': 'float',
          'default': 1,
          'description': 'Will not be (re)moved until this seed ratio is met.',
        },
        {
          'name': 'seed_time',
          'label': 'Seed time',
          'type': 'int',
          'default': 48,
          'description': 'Will not be (re)moved until this seed time (in hours) is met.',
        },
        {
          'name': 'extra_score',
          'advanced': True,
          'label': 'Extra Score',
          'type': 'int',
          'default': 0,
          'description': 'Starting score for each release found via this provider.',
        }
      ],
    },
  ],
}]
