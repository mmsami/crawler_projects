from xml.etree import ElementTree
import dateutil.parser as parser
import re
import json
import os
import urllib
import sys
from cStringIO import StringIO


def parsedata():
    source = 'S source_s Medicine Plus'
    type = 'S type_t Health Topic'

    document = ElementTree.parse('healthtopic.xml')
    # root = document.getroot()
    # published_date = 'S pubdate_dt'
    # print root.get('date-generated')
    for topic in document.findall('health-topic'):
        url = topic.attrib['url'].strip()
        language = 'S language_s ' + topic.attrib['language']
        title = 'S title_t ' + topic.attrib['title']
        article_id = 'S articleid_s ' + topic.attrib['id']
        date = 'S pubdate_dt ' + covertstringtoisodate(topic.attrib['date-created'])
        related_terms = 'S relatedterms_txt '
        mesh_json = ''
        summary_text = 'S summary_txt '
        group_text = 'S group_txt '
        group_json = 'S group_json_ss '
        language_mapped_txt = 'S language_mapped_topic_txt '
        language_mapped_json = 'S language_mapped_topic_json_ss '
        primary_institute_txt = ''
        primary_institute_json = ''
        related_topics_text = ''
        related_topics_json = ''
        reference_txt = ''
        site_txt = 'S site_txt '
        site_json = 'S site_json_ss '
        file_str = StringIO()
        for node in topic.getchildren():
            if node.tag == 'also-called':
                related_terms += node.text + '^'

            # if node.tag == 'mesh-heading':
            #     for childs in node.getchildren():
            #         if childs.tag == 'descriptor':
            #             txt = childs.text
            #             id = childs.attrib['id']
            #             mesh_txt = mesh_txt + '"title":' + '"' + txt + '", "id":"' + id + '"}'

            if node.tag == 'full-summary':
                text = re.sub(' +', ' ', node.text.replace('\n', ' ').replace('\r', ''))
                summary_text += text

            if node.tag == 'group':
                group_url = node.attrib['url']
                group_id = node.attrib['id']
                group_title = node.text
                group_text += group_title + '^'
                json_txt = '{"url":"' + group_url + '", "title":"' + node.text + '", "id":' + group_id + '}^'
                group_json += json_txt

            if node.tag == 'language-mapped-topic':
                language_mapped_txt += re.sub(' +', ' ', node.text.replace('\n', ' ').replace('\r', '').strip())
                language_url = node.attrib['url']
                language_id = node.attrib['id']
                language_mapped = node.attrib['language']
                language_text = node.text.strip()
                json_txt = '{"url":"' + language_url + '", "title":"' + language_text + '", "id":' + language_id + \
                           ', "language":"' + language_mapped + '"}^'
                language_mapped_json += json_txt

            if node.tag == 'primary-institute':
                primary_txt = re.sub(' +', ' ', node.text.replace('\n', ' ').replace('\r', '').strip())
                if primary_txt != '':
                    primary_institute_txt = 'S primary_institute_txt ' + primary_txt
                    primary_url = node.attrib['url']
                    json_txt = '{"url":"' + primary_url + '", "title":"' + primary_txt + '"}^'
                    primary_institute_json = 'primary_institute_json_ss ' + json_txt

            # if node.tag == 'see-reference':
            #     reference_txt += re.sub(' +', ' ', node.text.replace('\n', ' ').replace('\r', '').strip())

            if node.tag == 'site':
                all_titles = []
                all_titles.append(node.attrib['title'])
                all_title_set = set(all_titles)
                for s in all_title_set:
                    site_txt += s + '^'
                    #     # node_url = node.attrib['url']
                    #     # node_title = node.attrib['title']
                    #     # node_category = []
                    #     # node_string = ''
                    #     for childs in node:
                    #         node_url = childs.attrib['url']
                    #         print node_url
        for items in topic.iter('see-reference'):
            ref_tag = items.tag
            if ref_tag == 'see-reference':
                reference_txt += items.text + '^'

        for items in topic.iter('mesh-heading'):
            mesh_attributes = items.find('descriptor').attrib
            mesh_txt = items.find('descriptor').text
            mesh_attributes['title'] = mesh_txt
            mesh_json += convertjson(mesh_attributes)

        for items in topic.iter('related-topic'):
            topics_attributes = items.attrib
            topics_text = items.text
            topics_attributes['topic'] = topics_text
            related_topics_json += convertjson(topics_attributes)
            related_topics_text += topics_text + '^'

        for sites in topic.iter('site'):
            sites_attributes = sites.attrib
            category_tag = sites.findall('information-category')
            category_size = len(category_tag)
            organization_tag = sites.findall('organization')
            organization_size = len(organization_tag)
            description_tag = sites.findall('standard-description')
            description_size = len(description_tag)

            if category_size == 1:
                sites_attributes['category'] = category_tag[0].text
            if category_size > 1:
                category_list = []
                for category in category_tag:
                    category_list.append(category.text)
                    sites_attributes['category'] = category_list

            if organization_size == 1:
                sites_attributes['organization'] = organization_tag[0].text
            if organization_size > 1:
                organization_list = []
                for organization in organization_tag:
                    organization_list.append(organization.text)
                    sites_attributes['organization'] = organization_list

            if description_size == 1:
                sites_attributes['description'] = description_tag[0].text
            if description_size > 1:
                description_list = []
                for description in description_tag:
                    description_list.append(description.text)
                    sites_attributes['description'] = description_list

            file_str.write((convertjson(sites_attributes)))
            # site_json = site_json.join(convertjson(sites_attributes))

        related_terms = removelaststring(related_terms)
        group_text = removelaststring(group_text)
        group_json = group_json[:-1]
        language_mapped_json = language_mapped_json[:-1]
        primary_institute_json = primary_institute_json[:-1]
        site_txt = site_txt[:-1]
        site_json = site_json + removelaststring(file_str.getvalue())
        if reference_txt != '':
            reference_txt = 'S see_reference_txt ' + removelaststring(reference_txt)
        if mesh_json != '':
            mesh_json = 'S mesh_json_ss ' + removelaststring(mesh_json)
        if related_topics_json != '':
            related_topics_json = 'S related_topic_json_ss ' + removelaststring(related_topics_json)
        if related_topics_text != '':
            related_topics_text = 'S related_topic_txt ' + removelaststring(related_topics_text)
        # print site_json
        file_str.close()

        # injector_file_String = url + '|' + language + '|' + title + '|' + article_id + '|' + date + '|' + \
        #                        related_terms + '|' + mesh_txt + '|' + summary_text + '|' + group_text + '|' + group_json + \
        #                        '|' + language_mapped_txt + '|' + language_mapped_json + '|' + primary_institute_txt + '|' + \
        #                        primary_institute_json + '|' + reference_txt + '|' + site_txt + '|' + site_json
        # print injector_file_String
        injector_file_list = [url, language, title, article_id, date, related_terms, mesh_json, summary_text,
                              group_text, group_json, language_mapped_txt, language_mapped_json, primary_institute_txt,
                              primary_institute_json, related_topics_text, related_topics_json, reference_txt, site_txt,
                              site_json]
        injector_file_string = "|".join(filter(None, injector_file_list))
        print injector_file_string

        writetofile(injector_file_string)


def covertstringtoisodate(datestring):
    date = (parser.parse(datestring))
    return str(date.isoformat() + 'Z')


def convertjson(dictionary):
    return str(json.dumps(dictionary)) + '^'


def removelaststring(data):
    return data[:-1]


def writetofile(data):
    with open('injector_file.txt', 'a') as f:
        f.write(data + '\n')


def deletefile(filename):
    if os.path.exists(filename):
        os.remove(filename)


def downloadxmlfile(url):
    print 'Downloading xml: '
    urllib.urlretrieve(url, filename='healthtopic.xml')


if __name__ == '__main__':
    injector_file_name = 'injector_file.txt'
    xml_file_name = 'healthtopic.xml'
    reload(sys)
    sys.setdefaultencoding('utf-8')
    deletefile(injector_file_name)
    # downloadxmlfile('https://www.nlm.nih.gov/medlineplus/xml/mplus_topics_2016-05-03.xml')
    parsedata()
