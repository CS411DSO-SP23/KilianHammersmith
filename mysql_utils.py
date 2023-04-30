import pymysql
import numpy
import pandas as pd
def connection():
    db = pymysql.connect(host='127.0.0.1',
                                user='root',
                                password='Kilian1998',
                                database='academicworld',
                                charset='utf8mb4',
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor)
    return db

def get_universities():
    db = connection()
    with db.cursor() as cursor:
        sql = 'select name from university order by name'
        cursor.execute(sql)
        result = cursor.fetchall()
        uni_names = []
        for u in result:
            uni_names.append(u["name"])
    db.close()
    return uni_names

# return all faculty from the selected university
# take data and return it into a list to display
def get_faculty_names(uni_value):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select f.name as Name from faculty f, university u where\
            u.name ="' + str(uni_value) + '" \
            and f.university_id = u.id;'
        cursor.execute(sql)
        result = cursor.fetchall()
        fac_names = []
        for f in result:
            fac_names.append(f["Name"])
    db.close()
    return fac_names
    

# return faculty information
# maybe return faculty image
def get_faculty_info_position (prof_value):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select position from faculty where name = "'+ prof_value + '";'
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()
    return result[0]['position']

def get_faculty_info_email (prof_value):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select email from faculty where name = "'+ prof_value + '";'
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()
    return result[0]['email']
    
def get_faculty_info_phone (prof_value):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select phone from faculty where name = "'+ prof_value + '";'
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()
    return result[0]['phone']
    
def get_faculty_info_interst (prof_value):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select research_interest from faculty where name = "'+ prof_value + '";'
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()
    return result[0]['research_interest']
    
def get_faculty_info_photo (prof_value):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select photo_url from faculty where name = "'+ prof_value + '";'
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()
    return result[0]['photo_url']

# rank the faculty at a picked univeristy in their KRC for a desired keyword
# when this is added to the dashboard, make sure to include a description of KRC
def get_faculty_rank_keyword(u_name, k_name):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select f.name, sum(pk.score * p.num_citations) as KRC\
            from publication_keyword pk, keyword k, faculty_publication fp,\
            publication p, faculty f, university u \
            where u.name = "' + u_name + '" and f.university_id = u.id\
            and f.id = fp.faculty_id and p.id = pk.publication_id\
            and pk.publication = fp.publication_id and k.id = pk.keyword_id\
            and k.name = "'+ k_name +'" group by f.id order by KRC desc'
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()
    return result

# get the title and the number of citations of the publications from a faculty
# add keyword to make search more relevant
def get_publications (prof_name):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select p.title, p.num_citations from faculty f, faculty_publication fp,\
            publication p  where f.name = "' + prof_name + '" and fp.faculty_id = f.id and \
                p.id = fp.publication_id order by p.num_citations desc limit 1;'
        cursor.execute(sql)
        result = cursor.fetchall()
    db.close()
    return result
    

def keywords_by_year(u_name, k_name):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select p.year, count(p.title) from publication p, publication_keyword pk, keyword k,\
        faculty f, university u, faculty_publication fp where u.name = "'+ str(u_name) +'"\
        and f.university_id = u.id and fp.faculty_id = f.id\
        and fp.publication_id = p.id and pk.publication_id = p.id and pk.keyword_id = k.id \
        and k.name = "' + str(k_name) + '" group by p.year order by p.year;'
        cursor.execute(sql)
        result = cursor.fetchall()      
        dict = {'year':[], 'count':[]}
        for i in result:
            dict['year'].append(i['year'])
            dict['count'].append(i['count(p.title)'])
        db.close()
    return dict
    
# add a row to the faculty column based on the univeristy 
# first get univeristy 
def add_faculty(u_name, f_id, f_name, f_position, f_research_interest, f_email, f_phone, f_photo_url):
    db = connection()
    try:
        with db.cursor() as cursor:
            sql = 'insert into faculty values (' + str(f_id) + ', ' + str(f_name) +', '+ str(f_position) +', '+str(f_research_interest)+', '+ str(f_email)+', '+ str(f_phone) +', '+ str(f_photo_url) +', (select id from university where name = "'+u_name+'"));'
            cursor.execute(sql)
            db.close()
    except:
        return ['error']
def get_keywords():
    db = connection()
    with db.cursor() as cursor:
        sql = 'select name from keyword'
        cursor.execute(sql)
        results = cursor.fetchall()
        keyword_names = []
        for k in results:
            keyword_names.append(k['name'])
    db.close()
    return keyword_names
    
def get_uID_from_uName(u_name):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select id from university where name like "' + u_name + '";'
        cursor.execute(sql)
        result = cursor.fetchall()
        print(len(result))
        if len(result) == 0:
            return 'not found'
        u_id = result[0]['id']
    db.close()
    return u_id
    
def get_count_faculty():
    db = connection()
    with db.cursor() as cursor:
        sql = 'select count(name) from faculty'
        cursor.execute(sql)
        result = cursor.fetchall()
        count = result[0]['count(name)']
    db.close()
    return count
    
def remove_faculty(u_id, f_name):
    db = connection()
    with db.cursor() as cursor:
        sql = 'delete from faculty where name = "' + f_name + '" and university_id = "' + u_id + '";'
        cursor.execute(sql)
    db.close()

def add_trigger_faculty():
    db = connection()
    with db.cursor() as cursor:
        sql = 'CREATE TRIGGER InsertPreventTrigger BEFORE INSERT ON faculty\
            FOR EACH ROW\
            BEGIN\
            IF(new.university_id not in (select id from university)) THEN\
            SIGNAL SQLSTATE \'45000\'\
            SET MESSAGE_TEXT = "You can not insert record";\
            END IF;\
            END;'
        cursor.execute(sql)
    db.close()


def add_fac_keyword_score_view():
    db = connection()
    with db.cursor() as cursor:
        sql = 'create view faculty_keyword_score\
            as select f.name as faculty, k.name as keyword, fk.score from faculty f, keyword k, faculty_keyword fk\
            where f.id = fk.faculty_id\
            and k.id = fk.keyword_id;'
        cursor.execute(sql)
    db.close()

def add_uni_index():
    db = connection()
    with db.cursor() as cursor:
        sql = 'create index uni_name on university(name);'
        cursor.execute(sql)
    db.close()

def fac_uID_null():
    db = connection()
    with db.cursor() as cursor:
        sql = 'alter table faculty modify university_id int not null;'
        cursor.execute(sql)
    db.close()

def get_fac_from_view():
    db = connection()
    with db.cursor() as cursor:
        sql = 'select distinct faculty from faculty_keyword_score;'
        cursor.execute(sql)
        result = cursor.fetchall()
        names = []
        for i in result:
            names.append(i['faculty'])
    db.close()
    return names

def get_fac_keyword_scores(fac_name):
    db = connection()
    with db.cursor() as cursor:
        sql = 'select keyword, score from faculty_keyword_score\
            where faculty = "' + str(fac_name) + '";'
        cursor.execute(sql)
        result = cursor.fetchall()
        dict = {'keyword':[], 'score':[]}
        for i in result:
            dict['keyword'].append(i['keyword'])
            dict['score'].append(i['score'])
    db.close()
    return dict

def get_all_pubs():
    db = connection()
    with db.cursor() as cursor:
        sql = 'select title from publication;'
        cursor.execute(sql)
        result = cursor.fetchall()
        titles = []
        for i in result:
            titles.append(i['title'])
    db.close()
    return titles
    
    
def add_keyword(title, keyword, score):
    db = connection()
    with db.cursor() as cursor:
        sql = 'insert into publication_keyword\
            values((select id from publication where title = "' + title + '"),\
                (select id from keyword where name = "' + keyword + '"), ' + score + ');'
        cursor.execute(sql)
    db.close()

