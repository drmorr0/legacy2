import simplejson
from collections import OrderedDict
from flask import request
from flask import make_response


def load_saved_visible_categories():
    visible_categories_str = request.cookies.get('categories')
    if visible_categories_str:
        for category in list(VISIBLE_CATEGORIES):
            set_category_visibility(category, False)
        visible_categories = simplejson.loads(visible_categories_str)
        for category in visible_categories:
            set_category_visibility(category)


def is_valid_category(key):
    for group in CATEGORY_DICT.values():
        if key in group:
            return True

    return False


def set_category_visibility(key, visible=True):
    for group in CATEGORY_DICT.values():
        if key in group:
            group[key][1] = visible
            if visible:
                VISIBLE_CATEGORIES.add(key)
            else:
                VISIBLE_CATEGORIES.remove(key)


def get_category_string(key):
    for group in CATEGORY_DICT.values():
        if key in group:
            return group[key][0]

    return None


def get_visible_category_strings():
    strings = []
    for group in CATEGORY_DICT.values():
        for key, (string, visible) in group.items():
            if visible:
                strings.append((key, string))

    return sorted(strings)


VISIBLE_CATEGORIES = set(['MEMBTOT', 'AVATTWOR'])
CATEGORY_DICT = OrderedDict([
    ('Membership', 
        OrderedDict([
            ('MEMBTOT', ['Total Membership', True]),
            ('RECPROF', ['Members Received on Profession of Faith', False]),
            ('RECREST', ['Members Restored by Affirmation', False]),
            ('RECUMC', ['Members Transferred from other UM churches', False]),
            ('RECOTH', ['Members Transferred from non-UM churches', False]),
            ('REMCHR', ['Members Removed by Conference Action', False]),
            ('REMWITH', ['Withdrawn Members', False]),
            ('REMUMC', ['Members Transferring to other UM churches', False]),
            ('REMOTH', ['Members Transferring to other non-UM churches', False]),
            ('REMDEATH', ['Members Who Have Died', False]),
            ('MEMBPREV', ['Previous Year Membership Total', False]),
            ('RECCOR', ['Additive Previous Year Membership Corrections', False]),
            ('REMCOR', ['Subtractive Previous Year Membership Corrections', False]),
            ('MEMBFEM', ['Male Members', False]),
            ('MEMBMALE', ['Female Members', False]),
            ('MEMBA', ['Asian Members', False]),
            ('MEMBAAB', ['African American/Black Members', False]),
            ('MEMBH', ['Hispanic Members', False]),
            ('MEMBN', ['Native American Members', False]),
            ('MEMBP', ['Pacific Islander Members', False]),
            ('MEMBW', ['Caucasian Members', False]),
            ('MEMBMR', ['Multi-Racial Members', False]),
        ])
    ),

    ('Attendance',
        OrderedDict([
            ('AVATTWOR', ['Average Worship Attendance', True]),
            ('CSATTSUN', ['Average Sunday School Attendance', False]),
            ('CFTOTAL', ['Total Christian Formation/Small Group Attendance', False]),
            ('CFCHILD', ['Children in Christian Formation/Small Groups', False]),
            ('CFYOUTH', ['Youth in Christian Formation/Small Groups', False]),
            ('CFYADLT', ['Young Adults in Christian Formation/Small Groups', False]),
            ('CFOADLT', ['Adults in Christian Formation/Small Groups', False]),
            ('CONFIRM', ['Enrollment in Confirmation Classes', False]),
            ('VBSPART', ['VBS Participants', False]),
        ]),
    ),

    ('Baptism',
        OrderedDict([
            ('NUMBAPT', ['Total Baptisms', False]),
            ('BAPTCHILD', ['Children Baptized', False]),
            ('BAPTADULT', ['Adults Baptized', False]),
            ('PREPMEMB', ['Baptized Members who have not become Professing Members', False]),
        ]),
    ),

    ('Missions',
        OrderedDict([
            ('UMVIM', ['UMVIM Teams', False]),
            ('UMVIMPAR', ['Persons on UMVIM Teams', False]),
            ('MISSENGAGE', ['Persons Engaged in Missions', False]),
            ('DAYSRVD', ['Number of Persons Served by Community Daycare/Education', False]),
            ('OUTSRVD', ['Number of Persons Served by Community Outreach', False]),
            ('UMMMEMB', ['Membership in UMM', False]),
            ('UMWMEMB', ['Membership in UMW', False]),
            ('UMMPROG', ['Amount Paid for UMM Projects', False]),
            ('UMWWORK', ['Amount Paid for UMW Projects', False]),
        ]),
    ),

    ('Assets',
        OrderedDict([
            ('VALPROP', ['Market Value of Church Property', False]),
            ('VALOTH', ['Market Value of Other Assets', False]),
            ('DEBTCHUR', ['Debt Secured by Physical Assets', False]),
            ('DEBTOTH', ['Other Debt', False]),
        ]),
    ),

    ('Expenditures', 
        OrderedDict([
            ('GRANDTOT', ['Total Expenditures Paid', False]),
            ('TOTAPP', ['Total Apportionments', False]),
            ('APPPAID', ['Total Apportionments Paid', False]),
            ('GENADV', ['General Advance Specials Paid', False]),
            ('WSSPEC', ['World Service Specials Paid', False]),
            ('CONFADV', ['Annual Conference Advance Specials Paid', False]),
            ('YSF', ['Youth Service Fund Paid', False]),
            ('BENOTHA', ['Other Funds Paid', False]),
            ('ACSPSUN', ['Special Sunday Offerings Paid', False]),
            ('UMDIRECT', ['Given Directly to UM causes', False]),
            ('OTHDIRECT', ['Given Directly to non-UM causes', False]),
            ('GENCHROF', ['General Special Sunday Offerings Paid', False]),
            ('PENBILLED', ['Pension Benefits Paid', False]),
            ('HLTHBILLED', ['Healthcare Benefits Paid', False]),
            ('COMPPAST', ['Pastor Base Compensation', False]),
            ('COMPASSC', ['Associate Pastor Base Compensation', False]),
            ('TOTPAST', ['Housing Expenses', False]),
            ('TOTREMB', ['Reimbursments', False]),
            ('TOTCASH', ['Cash Allowances', False]),
            ('DEACOMP', ['Deacon Salary and Benefits', False]),
            ('OTHCOMP', ['Other Salary and Benefits', False]),
            ('PROGEXP', ['Local Church Program Expenses', False]),
            ('OPEREXP', ['Operating Expenses', False]),
            ('PRININT', ['Debts Paid', False]),
            ('BLDGIMPV', ['Capital Expenditures', False]),
            ('RENTAL', ['Parsonage Rental Paid', False]),
        ]),
    ),

    ('Giving',
        OrderedDict([
            ('NUMPLEDG', ['Households Giving to Church', False]),
            ('ANNOPP', ['Total Income Received for Budget', False]),
            ('BENOTHAa', ['Funds Received Through Pledges', False]),
            ('BENOTHAb', ['Funds Received from Identified Givers', False]),
            ('BENOTHAc', ['Funds Received from Unidentified Givers', False]),
            ('BENOTHAd', ['Funds Received from Interest and Dividends', False]),
            ('BENOTHAe', ['Funds Received from Sale of Assets', False]),
            ('BENOTHAf', ['Funds Received from Building Use Fees', False]),
            ('BENOTHAg', ['Other Sources of Income', False]),
            ('CAPFUN', ['Total Income Received for Capital Campaigns and Projects', False]),
            ('CAPFUNa', ['Funds Received from Capital Campaigns', False]),
            ('CAPFUNb', ['Funds Received from Memorials', False]),
            ('CAPFUNc', ['Funds Received from Other Projects', False]),
            ('CAPFUNd', ['Funds Received from Special Sundays Giving', False]),
            ('FUNDSCR', ['Total Income From Outside the Church', False]),
            ('FUNDSCRa', ['Equitable Compensation Funds Received', False]),
            ('FUNDSCRb', ['Advance Special Funds Received', False]),
            ('FUNDSCRc', ['Grants and Institutional Support Received', False]),
        ]),
    ),

    ('Miscellaneous',
        OrderedDict([
            ('CONSTIT', ['Other Church Constituents', False]),
            ('CSCLASS', ['Sunday School Classes', False]),
            ('ONGOCLASS', ['Other Ongoing Classes', False]),
            ('SHORTCLASS', ['Short-Term Classes and Groups', False]),
            ('CSATTSHT', ['Average Attendance in Short-Term Classes', False]),
            ('UMYFMEMB', ['United Methodist Youth Membership', False]),
            ('UMYFPROJ', ['Amount Paid for UMYF Projects', False]),
            ('UMWTREAS', ['Amount Paid to UMW Treasurer', False]),
        ]),
    ),
])
