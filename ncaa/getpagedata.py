# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import datetime
import psycopg2
import configuration
import requests
import random
import sys
import time

user_agents = [
    {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'},
    {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'},
    {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'},
    {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'}]

base_url = 'https://web3.ncaa.org/hsportal/exec/hsAction'

codesfile = 'codes.txt'
pagedatafile = 'pagedata.html'


def getapprovedtable(soup, id, subject, ncaa_code):
    hs_course_list = []
    approvedtable = soup.find('table', {'id': id})
    if approvedtable.find('td', {'class': 'hs_tableData'}) is None:
        rows = approvedtable.find_all('tr')[1:]
        for x in rows:
            cells = x.find_all('td')
            if len(cells) == 6:
                approved_courses_dict = {}
                approved_courses_dict['course_weight'] = cells[0].text.strip()
                approved_courses_dict['title'] = cells[1].text.strip()
                approved_courses_dict['notes'] = cells[2].text.strip()
                approved_courses_dict['lab'] = ''
                approved_courses_dict['max_credits'] = cells[3].text.strip()
                approved_courses_dict['ok_through'] = cells[4].text.strip()
                approved_courses_dict['disability_course'] = cells[5].text.strip()
                approved_courses_dict['subject'] = subject
                approved_courses_dict['course_status'] = 'Approved'
                approved_courses_dict['ncaa_code'] = ncaa_code
                approved_courses_dict['reason_code'] = ''
                hs_course_list.append(approved_courses_dict)
            if len(cells) == 7:
                approved_courses_dict = {}
                approved_courses_dict['course_weight'] = cells[0].text.strip()
                approved_courses_dict['title'] = cells[1].text.strip()
                approved_courses_dict['notes'] = cells[2].text.strip()
                approved_courses_dict['lab'] = cells[3].text.strip()
                approved_courses_dict['max_credits'] = cells[4].text.strip()
                approved_courses_dict['ok_through'] = cells[5].text.strip()
                approved_courses_dict['disability_course'] = cells[6].text.strip()
                approved_courses_dict['subject'] = subject
                approved_courses_dict['course_status'] = 'Approved'
                approved_courses_dict['ncaa_code'] = ncaa_code
                approved_courses_dict['reason_code'] = ''
                hs_course_list.append(approved_courses_dict)
    return hs_course_list


def getdeniedtable(soup, id, subject, ncaa_code):
    hs_course_list = []
    deniedtable = soup.find('table', {'id': id})
    if deniedtable.find('td', {'class': 'hs_tableData'}) is None:
        rows = deniedtable.find_all('tr')[1:]
        for x in rows:
            cells = x.find_all('td')
            if len(cells) == 7:
                denied_courses_dict = {}
                denied_courses_dict['course_weight'] = cells[0].text.strip()
                denied_courses_dict['title'] = cells[1].text.strip()
                denied_courses_dict['notes'] = cells[2].text.strip()
                denied_courses_dict['lab'] = ''
                denied_courses_dict['max_credits'] = cells[3].text.strip()
                denied_courses_dict['ok_through'] = cells[4].text.strip()
                denied_courses_dict['reason_code'] = cells[5].text.strip()
                denied_courses_dict['disability_course'] = cells[6].text.strip()
                denied_courses_dict['subject'] = subject
                denied_courses_dict['course_status'] = 'Denied'
                denied_courses_dict['ncaa_code'] = ncaa_code
                hs_course_list.append(denied_courses_dict)
            if len(cells) == 8:
                denied_courses_dict = {}
                denied_courses_dict['course_weight'] = cells[0].text.strip()
                denied_courses_dict['title'] = cells[1].text.strip()
                denied_courses_dict['notes'] = cells[2].text.strip()
                denied_courses_dict['lab'] = cells[3].text.strip()
                denied_courses_dict['max_credits'] = cells[4].text.strip()
                denied_courses_dict['ok_through'] = cells[5].text.strip()
                denied_courses_dict['reason_code'] = cells[6].text.strip()
                denied_courses_dict['disability_course'] = cells[7].text.strip()
                denied_courses_dict['subject'] = subject
                denied_courses_dict['course_status'] = 'Denied'
                denied_courses_dict['ncaa_code'] = ncaa_code
                hs_course_list.append(denied_courses_dict)
    return hs_course_list


def getarchivedtable(soup, id, subject, ncaa_code):
    hs_course_list = []
    archivedtable = soup.find('table', {'id': id})
    if archivedtable.find('td', {'class': 'hs_tableData'}) is None:
        rows = archivedtable.find_all('tr')[1:]
        for x in rows:
            cells = x.find_all('td')
            if len(cells) == 6:
                archived_courses_dict = {}
                archived_courses_dict['course_weight'] = cells[0].text.strip()
                archived_courses_dict['title'] = cells[1].text.strip()
                archived_courses_dict['notes'] = cells[2].text.strip()
                archived_courses_dict['lab'] = ''
                archived_courses_dict['max_credits'] = cells[3].text.strip()
                archived_courses_dict['ok_through'] = cells[4].text.strip()
                archived_courses_dict['disability_course'] = cells[5].text.strip()
                archived_courses_dict['subject'] = subject
                archived_courses_dict['course_status'] = 'Archived'
                archived_courses_dict['ncaa_code'] = ncaa_code
                archived_courses_dict['reason_code'] = ''
                hs_course_list.append(archived_courses_dict)
            if len(cells) == 7:
                archived_courses_dict = {}
                archived_courses_dict['course_weight'] = cells[0].text.strip()
                archived_courses_dict['title'] = cells[1].text.strip()
                archived_courses_dict['notes'] = cells[2].text.strip()
                archived_courses_dict['lab'] = cells[3].text.strip()
                archived_courses_dict['max_credits'] = cells[4].text.strip()
                archived_courses_dict['ok_through'] = cells[5].text.strip()
                archived_courses_dict['disability_course'] = cells[6].text.strip()
                archived_courses_dict['subject'] = subject
                archived_courses_dict['course_status'] = 'Archived'
                archived_courses_dict['ncaa_code'] = ncaa_code
                archived_courses_dict['reason_code'] = ''
                hs_course_list.append(archived_courses_dict)
    return hs_course_list


def getschoolyear():
    currentYear = datetime.datetime.now().year
    return str(currentYear) + '-' + str(currentYear + 1)


def parsedata():
    hs_info_dict = {}
    hs_course_list = []
    with open(pagedatafile) as f:
        pagedata = f.read()
        soup = BeautifulSoup(pagedata, "html.parser")
        # Account status
        statustable = soup.find('div', {'id': 'hsAccountStatusDscrDiv'}).find('table', {'cellspacing': '1'})
        statustablerows = statustable.find_all('tr')
        for eachrow in statustablerows:
            status = eachrow.find('td', {'class': 'showGrayBubbleMsgClass'})
            if status is not None:
                hs_info_dict['account_status'] = eachrow.find_all('td')[1].text.strip()
        # HS Information Table
        infotable = soup.find('div', {'id': 'hsInfo'}).find_all('table', {'cellspacing': '0'})[1].find('table')
        infocells = infotable.find_all('td', {'class': 'tdTinyFontForWsrDetail'})
        hs_info_dict['ncaa_code'] = infocells[0].text.strip()
        hs_info_dict['ceeb_code'] = infocells[1].text.strip()
        hs_info_dict['high_school_name'] = infocells[2].text.strip()
        hs_info_dict['primary_contact_name'] = infocells[4].text.strip()
        hs_info_dict['primary_contact_phone'] = infocells[5].text.strip()
        hs_info_dict['primary_contact_fax'] = infocells[6].text.strip()
        hs_info_dict['primary_contact_email'] = infocells[7].text.strip()
        hs_info_dict['secondary_contact_name'] = infocells[8].text.strip()
        hs_info_dict['secondary_contact_phone'] = infocells[9].text.strip()
        hs_info_dict['secondary_contact_fax'] = infocells[10].text.strip()
        hs_info_dict['secondary_contact_email'] = infocells[11].text.strip()
        hs_info_dict['school_website'] = infocells[12].text.strip()
        hs_info_dict['link_course_catalog'] = infocells[13].text.strip()
        hs_info_dict['last_update_date'] = infocells[14].text.strip()

        address_string = infocells[3]
        for e in address_string.find_all('br'):
            e.replace_with('|')
        address_list = [x.strip() for x in address_string.text.split('|')]
        hs_info_dict['address'] = address_list[0]
        hs_info_dict['city'] = address_list[1]
        try:
            hs_info_dict['state'] = address_list[2].split('-')[0].strip()
        except IndexError:
            hs_info_dict['state'] = ''
        try:
            hs_info_dict['zip'] = address_list[2].split('-')[1].strip()
        except IndexError:
            hs_info_dict['zip'] = ''

            # Approved Courses
        # approvedenglishtable = soup.find('table', {'id': 'approvedCourseTable_1'})
        # if approvedenglishtable.find('td', {'class': 'hs_tableData'}) is None:
        #     rows = approvedenglishtable.find_all('tr')[1:]
        approved_course_list_english = getapprovedtable(soup, 'approvedCourseTable_1', 'English',
                                                        hs_info_dict['ncaa_code'])
        approved_course_list_social_science = getapprovedtable(soup, 'approvedCourseTable_2', 'Social Science',
                                                               hs_info_dict['ncaa_code'])
        approved_course_list_mathematics = getapprovedtable(soup, 'approvedCourseTable_3', 'Mathematics',
                                                            hs_info_dict['ncaa_code'])
        approved_course_natural_physical_science = getapprovedtable(soup, 'approvedCourseTable_4',
                                                                    'Natural/Physical Science',
                                                                    hs_info_dict['ncaa_code'])
        approved_course_additional_core_courses = getapprovedtable(soup, 'approvedCourseTable_5',
                                                                   'Additional Core Courses', hs_info_dict['ncaa_code'])

        denied_course_list_english = getdeniedtable(soup, 'deniedCourseTable_1', 'English',
                                                    hs_info_dict['ncaa_code'])
        denied_course_list_social_science = getdeniedtable(soup, 'deniedCourseTable_2', 'Social Science',
                                                           hs_info_dict['ncaa_code'])
        denied_course_list_mathematics = getdeniedtable(soup, 'deniedCourseTable_3', 'Mathematics',
                                                        hs_info_dict['ncaa_code'])
        denied_course_list_physical_science = getdeniedtable(soup, 'deniedCourseTable_4', 'Natural/Physical Science',
                                                             hs_info_dict['ncaa_code'])
        denied_course_list_additional_core_courses = getdeniedtable(soup, 'deniedCourseTable_5',
                                                                    'Additional Core Courses',
                                                                    hs_info_dict['ncaa_code'])

        archived_course_list_english = getarchivedtable(soup, 'ArchivedCourseTable_1', 'English',
                                                        hs_info_dict['ncaa_code'])
        archived_course_list_social_science = getarchivedtable(soup, 'ArchivedCourseTable_2', 'Social Science',
                                                               hs_info_dict['ncaa_code'])
        archived_course_list_mathematics = getarchivedtable(soup, 'ArchivedCourseTable_3', 'Mathematics',
                                                            hs_info_dict['ncaa_code'])
        archived_course_list_physical_science = getarchivedtable(soup, 'ArchivedCourseTable_4',
                                                                 'Natural/Physical Science', hs_info_dict['ncaa_code'])
        archived_course_list_additional_core_courses = getarchivedtable(soup, 'ArchivedCourseTable_5',
                                                                        'Additional Core Courses',
                                                                        hs_info_dict['ncaa_code'])

        hs_course_list = approved_course_list_english + approved_course_list_social_science + \
                         approved_course_list_mathematics + approved_course_natural_physical_science + \
                         approved_course_additional_core_courses + denied_course_list_english + \
                         denied_course_list_social_science + denied_course_list_mathematics + \
                         denied_course_list_physical_science + denied_course_list_additional_core_courses + \
                         archived_course_list_english + archived_course_list_social_science + \
                         archived_course_list_mathematics + archived_course_list_physical_science + \
                         archived_course_list_additional_core_courses

    return hs_info_dict, hs_course_list


def getdatabaseconnection():
    connection = psycopg2.connect("dbname=%s user=%s host=%s password=%s port=%s" % (configuration.db_name,
                                                                                     configuration.user,
                                                                                     configuration.host,
                                                                                     configuration.password,
                                                                                     configuration.port))
    if connection is not None:
        print 'Connected to Database'
    return connection


def savetodatabase(connection, school_info_dict, school_course_list):
    cursor = connection.cursor()
    crawl_date = datetime.datetime.now()
    schoolYear = getschoolyear()
    school_info_sql = '''INSERT INTO ncaa_school_info (crawl_date, account_status, ncaa_code, ceeb_code, high_school_name,
    address, city, state, zip, primary_contact_name, primary_contact_phone, primary_contact_fax, primary_contact_email,
    secondary_contact_name, secondary_contact_phone, secondary_contact_fax, secondary_contact_email,
    school_website, link_to_course_catalog, last_update_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s)'''
    course_info_sql = '''INSERT INTO ncaa_course_info (crawl_date, ncaa_code, high_school_name, school_year,
    course_status, subject, course_weight, title, notes, lab, max_credits, ok_through, disability_course, reason_code)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    if school_info_dict:
        print 'Inserting school info ' + str(school_info_dict)
        cursor.execute(school_info_sql, (crawl_date, school_info_dict['account_status'], school_info_dict['ncaa_code'],
                                         school_info_dict['ceeb_code'], school_info_dict['high_school_name'],
                                         school_info_dict['address'], school_info_dict['city'],
                                         school_info_dict['state'], school_info_dict['zip'],
                                         school_info_dict['primary_contact_name'].encode('utf-8'),
                                         school_info_dict['primary_contact_phone'],
                                         school_info_dict['primary_contact_fax'],
                                         school_info_dict['primary_contact_email'],
                                         school_info_dict['secondary_contact_name'].encode('utf-8'),
                                         school_info_dict['secondary_contact_phone'],
                                         school_info_dict['secondary_contact_fax'],
                                         school_info_dict['secondary_contact_email'],
                                         school_info_dict['school_website'],
                                         school_info_dict['link_course_catalog'], school_info_dict['last_update_date']))

    if school_course_list:
        for data in school_course_list:
            print 'Inserting course info ' + str(data)
            cursor.execute(course_info_sql, (crawl_date, data['ncaa_code'], school_info_dict['high_school_name'],
                                             schoolYear, data['course_status'], data['subject'], data['course_weight'],
                                             data['title'], data['notes'], data['lab'], data['max_credits'],
                                             data['ok_through'], data['disability_course'], data['reason_code']))

    connection.commit()
    print 'Records Updated'


def postrequest(code):
    rand_user_agent = random.choice(user_agents)
    with requests.Session() as session:
        response = session.post(base_url, headers=rand_user_agent, data={'hsActionSubmit': 'Search', 'hsCode': code})
        time.sleep(random.randint(2, 3))
        with open(pagedatafile, 'w') as pagefile:
            pagefile.write(response.text.encode('utf-8'))


def app(con, arglist):
    with open(codesfile, 'r') as cfile:
        for line in cfile:
            if line:
                state = line.split('|')[0].strip()
                code = line.split('|')[1].strip()
                if arglist:
                    if state in arglist:
                        postrequest(code)
                        school_info_dict, school_course_list = parsedata()
                        savetodatabase(con, school_info_dict, school_course_list)
                else:
                    postrequest(code)
                    school_info_dict, school_course_list = parsedata()
                    savetodatabase(con, school_info_dict, school_course_list)


if __name__ == '__main__':
    start = datetime.datetime.now()
    argcount = len(sys.argv)
    arglist = []
    if argcount > 1:
        for arg in sys.argv[1:]:
            arglist.append(arg)

    connection = getdatabaseconnection()
    try:
        app(connection, arglist)
    finally:
        if connection is not None:
            connection.close()
    print 'Elapsed Time: %s' % (datetime.datetime.now() - start)
