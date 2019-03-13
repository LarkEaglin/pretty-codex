import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen

from dataConnect import Element, Co_element, Attribute, Co_attribute, Herb, Sign, Co_sign, Planet, Co_planet, Base, init_sqlalchemy, engine
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy import select

headers = {"User-Agent": "my practice web program for an herbal class project. I can be contacted at lrkdxn@gmail.com"}

yellow = 'http://slavekiten.tripod.com/id20.html'
alternate = 'https://www.themagickalcat.com/Articles.asp?ID=242'

sauce = urlopen(yellow)
webPage = sauce.read()
soup = BeautifulSoup(webPage, "html.parser")

h3 = soup.find_all('h3')
attribute = h3[-1]
sign = h3[2]
element = h3[1]
planetary = h3[0]
category = None

Session = sessionmaker(bind = engine)
session = Session()
def add_to_session(potential_obj):
    session.add(potential_obj)
    session.commit()

def gather_section(section_title):
    body = section_title.parent.parent.find('tbody')
    section = body.find_all('tr')
    # print (section)
    return section

def parse_section(topic):
    parent_list = []
    herb_lists = []

    for parsed in topic:
        parent_cell = parsed.findNext('td')

        if parent_cell != None  :
            parented = parent_cell.text
            parented2 = parented.strip()
            parent = str(parented2)
            parent_list.append(parent)

            dependent_cell = parent_cell.findNext('td')
            dependents = dependent_cell.text                
            herbs = dependents.split(',')

            herbslist = []                
            i = 0
            while i < len(herbs):
                herb = herbs[i].strip()
                herb_str = str(herb)               
                herbslist.append(herb_str)
                
                i = i + 1
            # print herbslist
            herb_lists.append(herbslist)

    inserts = {}
    p = 0
    for k in parent_list:
        insert = {parent_list[p] : herb_lists[p]}
        inserts.update(insert)
        p = p + 1
    return inserts

def data_works(breakdown): 
    print('CHOSEN CATEGORY', str(category))
    temp_obj = None
    temp_herb = None
    collection = None

    for obj in breakdown:
        # obj is the dict key
        list_of_herbs = breakdown[obj]
        print('OBJECT: ', obj, '/ ', list_of_herbs)
    
        if category == element:
            temp_obj = Element(element_type = obj)
            add_to_session(temp_obj)  
        
        elif category == attribute:
                temp_obj = Attribute(attribute_type = obj)
                add_to_session(temp_obj)    

        elif category == planetary:
                temp_obj = Planet(planet_type = obj)
                add_to_session(temp_obj)    

        elif category == sign:
                temp_obj = Sign(sign_type = obj)
                add_to_session(temp_obj)    
            
        else:
                print('Alright then, try again.')

        print( 'Row for', temp_obj, 'created.')
        for herb_obj in list_of_herbs:
                herb_check = session.query(Herb).filter_by(name = herb_obj)
                herb_check_all = herb_check.all()

                if herb_check_all == []:
                    temp_herb = Herb(name = herb_obj)
                    add_to_session(temp_herb)
                else:
                    print('**HERB QUERY RESULT:', herb_check_all[0] )
                    # print(type(herb_check_all[0]))
                    result = herb_check_all[0]
                    temp_herb = result

                # el_collection_check = session.query(Co_element).filter_by(herb_id = temp_herb.herb_id).all()
                # attr_collection_check = session.query(Co_attribute).filter_by(herb_id = temp_herb.herb_id).all()
                # p_collection_check = session.query(Co_planet).filter_by(herb_id = temp_herb.herb_id).all()
                # sign_collection_check = session.query(Co_sign).filter_by(herb_id = temp_herb.herb_id).all()
                
                #  if attr_collection_check == []:
                #         collection = Co_attribute(herb=temp_herb, herb_name = temp_herb.herb_name, attribute_name = temp_obj.attribute , attribute=temp_obj)
                #     else:
                #         print(attr_collection_check)

                # Populate Association Table: collection
                if category == element:
                        collection = Co_element(herb=temp_herb, herb_name = temp_herb.name, element_type = temp_obj.element_type, element=temp_obj)     
                elif category == attribute:
                        collection = Co_attribute(herb=temp_herb, herb_name = temp_herb.name, attribute_type = temp_obj.attribute_type , attribute=temp_obj)
                elif category == planetary:
                        collection = Co_planet(herb=temp_herb, herb_name = temp_herb.name, planet_type = temp_obj.planet_type , planet=temp_obj)
                elif category == sign:
                        collection = Co_sign(herb=temp_herb, herb_name = temp_herb.name, sign_type = temp_obj.sign_type , sign=temp_obj)
                
                add_to_session(collection)
                print('*Added:', temp_herb, temp_obj, 'Association table id: ', collection.id)
        
        # print(collection)
        # session.commit()
        # print (obj, ': ', list_of_herbs) 
        #  print(str(collection.herb), 'is = ', htest.herb_name,  '*and is being mapped to --', collection.element)
            
# i tthink ill add a for loop that will have all of this information persist until its all gathered and commit it then..        
new = eval(input('Choose correspondence: \n *Attribute \n *Element \n **Sign \n *Planetary'))
category = new
# print('Category : ', new)

section = gather_section(new)
breakdown =parse_section(section)   
# print (breakdown)

data_works(breakdown)

# popcorn = session.query(Element)  #returns a Query object. 
# for oElement in popcorn:
    # print (oElement.name)












session.commit()
# session.close()