from enum import Enum


class EvenementType(str, Enum):
    INCENDIE = "incendie"
    CLIMATIQUE = "climatique"
    ATTENTAT = "attentat"
    ACCIDENT = "accident"
    ENLEVEMENT = "enlevement"
    EPIDEMIE = "epidemie"
    EXPLOSION = "explosion"
    RASSEMBLEMENT = "rassemblement"
    AUTRE = "autre"


EVENEMENT_TYPE_TO_CISU_CODE = {EvenementType.INCENDIE: ['C04.00.00',
                                                        'C04.01.00',
                                                        'C04.02.00',
                                                        'C04.03.00',
                                                        'C04.04.00',
                                                        'C04.05.00',
                                                        'C04.06.00',
                                                        'C04.07.00',
                                                        'C04.08.00',
                                                        'C04.09.00',
                                                        'C04.01.01',
                                                        'C04.01.02',
                                                        'C04.01.03',
                                                        'C04.01.04',
                                                        'C04.01.05',
                                                        'C04.01.06',
                                                        'C04.01.07',
                                                        'C04.01.08',
                                                        'C04.01.09',
                                                        'C04.01.10',
                                                        'C04.01.11',
                                                        'C04.02.01',
                                                        'C04.02.02',
                                                        'C04.02.03',
                                                        'C04.02.04',
                                                        'C04.07.01',
                                                        'C04.07.02',
                                                        'C04.07.03',
                                                        'C04.07.04',
                                                        'C02.07.03'],
                               EvenementType.ATTENTAT: ['C02.08.04',
                                                        'C02.08.05',
                                                        'C02.01.00',
                                                        'C07.01.00',
                                                        'C07.02.00',
                                                        'C07.09.00',
                                                        'C07.09.01',
                                                        'C07.09.02',
                                                        'C07.09.03',
                                                        'C07.09.04',
                                                        'C07.10.00',
                                                        'C07.11.00',
                                                        'C07.12.00',
                                                        'C02.08.04',
                                                        'C02.08.05'],
                               EvenementType.CLIMATIQUE: ['C08.00.00',
                                                          'C08.01.00',
                                                          'C08.02.00',
                                                          'C08.03.00',
                                                          'C08.04.00',
                                                          'C08.05.00',
                                                          'C08.06.00',
                                                          'C08.07.00',
                                                          'C08.08.00',
                                                          'C08.09.00',
                                                          'C08.10.00',
                                                          'C08.08.01',
                                                          'C08.08.02',
                                                          'C08.10.01',
                                                          'C02.07.01',
                                                          'C02.07.02',
                                                          'C02.10.00'],
                               EvenementType.ACCIDENT: ['C01.00.00',
                                                        'C01.01.00',
                                                        'C01.02.00',
                                                        'C01.03.00',
                                                        'C01.04.00',
                                                        'C01.05.00',
                                                        'C01.01.01',
                                                        'C01.01.02',
                                                        'C01.01.03',
                                                        'C01.01.04',
                                                        'C01.01.05',
                                                        'C01.01.06',
                                                        'C01.02.01',
                                                        'C01.02.02',
                                                        'C01.03.01',
                                                        'C01.03.02',
                                                        'C01.04.01',
                                                        'C01.04.02',
                                                        'C01.04.03',
                                                        'C01.04.04',
                                                        'C02.08.00',
                                                        'C02.08.01',
                                                        'C02.08.02',
                                                        'C02.08.03',
                                                        'C02.08.04',
                                                        'C02.08.05',
                                                        'C02.08.06',
                                                        'C02.08.07',
                                                        'C02.08.08',
                                                        'C02.09.00',
                                                        'C02.09.01',
                                                        'C02.09.02',
                                                        'C02.09.03',
                                                        'C02.09.04',
                                                        'C02.09.05',
                                                        'C02.09.06',
                                                        'C02.09.07'],
                               EvenementType.ENLEVEMENT: ['C02.04.00',
                                                          'C02.04.01',
                                                          'C02.04.02',
                                                          'C02.04.03'],
                               EvenementType.EPIDEMIE: ['C02.06.00', 'C02.06.01'],
                               EvenementType.EXPLOSION: ['C05.00.00',
                                                         'C05.01.00',
                                                         'C05.02.00',
                                                         'C05.03.00',
                                                         'C05.04.00',
                                                         'C05.05.00'],
                               EvenementType.RASSEMBLEMENT: ['C07.04.00',
                                                             'C07.04.01',
                                                             'C07.04.02',
                                                             'C07.04.03',
                                                             'C07.04.04',
                                                             'C07.05.00',
                                                             'C07.07.03',
                                                             'C07.13.04',
                                                             'C02.15.01']
                               }