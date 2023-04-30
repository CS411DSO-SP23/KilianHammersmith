import neo4j
import pandas

try:
    uri = "bolt://localhost:7687/cs411/academicworld"
    driver = neo4j.GraphDatabase.driver(uri, auth=('neo4j', 'Kilian1998!'))
except:
    print('unsuccesful')


def get_unis_neo4j():
    with driver.session(database='academicworld') as session:
        results = session.run('match (i:INSTITUTE) return i.name')
        records = list(results)
        uni_names = []
        for i in records:
            uni_names.append(i.data()['i.name'])
        return uni_names

def get_faculty_neo4j(u_name):
    with driver.session(database='academicworld') as session:
        results = session.run('match (f:FACULTY)-[:AFFILIATION_WITH]->(i:INSTITUTE where i.name = "' + str(u_name) + '") return f.name')
        records = list(results)
        fac_names = []
        for i in records:
            fac_names.append(i.data()['f.name'])
        return fac_names
    
def get_fac_publications_neo4j(fac_name, u_name):
    with driver.session(database='academicworld') as session:
        results = session.run('match (i:INSTITUTE where i.name = "'+ str(u_name) +'")-\
                              [:AFFILIATION_WITH]-(f:FACULTY where f.name = "'+ str(fac_name) +'")-[:PUBLISH]-(p:PUBLICATION)\
                                return p.title as Title, p.venue as Venue, p.year as Year, p.numCitations as `Number Citations`;')
        data = results.to_df()
        return data




