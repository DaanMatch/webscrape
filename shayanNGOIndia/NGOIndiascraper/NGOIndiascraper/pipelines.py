# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NgoindiascraperPipeline:
    def process_item(self, item, spider):
        return item
    #pipelines.py

from itemadapter import ItemAdapter
import psycopg2
from dotenv import load_dotenv
import os

class NgoIndiaScraperPipeline:

    def __init__(self):
        load_dotenv()  # load the variables from .env file
        HOST = os.getenv('DB_HOST')
        DATABASE = os.getenv('DB_NAME')
        USER = os.getenv('DB_USER')
        PASSWORD = os.getenv('DB_PASSWORD')
        # Connection parameters
        param_dic = {
            "host"      : HOST,
            "database"  : DATABASE,
            "user"      : USER,
            "password"  : PASSWORD
        }

        # Create/Connect to database
        self.connection = psycopg2.connect(**param_dic)

        # Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS NgoContact
        (
        NgoId UUID,
        NgoName text,
        OrgEmail text,
        OfficePhone text,
        PrimaryPoc text,
        PrimaryPocPhone text,
        SecondaryPoc text,
        SecondaryPocPhone text,
        MailingAddress text,
        PhysicalAddress text,
        FieldOffices text,
        OrgType text,
        OrgWebsite character varying(2048),
        Facebook character varying(2048),
        Twitter character varying(2048),
        Instagram character varying(2048),
        Youtube character varying(2048),
        Whatsapp text,
        OtherSocials text,
        ExecutiveDirector text,
        TechnicalSupport text,
        ChairmanName text,
        ChairmanMobile text,
        ChairmanEmail text,
        ViceChairmanName text,
        ViceChairmanMobile text,
        ViceChairmanEmail text,
        SecretaryName text,
        SecretaryMobile text,
        SecretaryEmail text,
        AssistantSecretaryName text,
        AssistantSecretaryMobile text,
        AssistantSecretaryEmail text
        )
        """)
    def process_item(self, item, spider):

        # Check to see if text is already in database 
        self.cur.execute("select * from NgoContact where ngoName = %s", (item['name'],))
        result = self.cur.fetchone()

        # If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['name'])

        # If ngo isn't in the DB, insert data
        else:
            # Define insert statement
            self.cur.execute(""" insert into NgoContact (ngoName, OrgEmail, OfficePhone, OrgWebsite, MailingAddress, PhysicalAddress, OrgType) 
                                values (%s,%s,%s,%s,%s,%s,%s)""", (
                item["name"],
                item["email"],
                item["telephone"],
                item["website"],
                item["address"],
                item["address"],
                item["ngoType"]
            ))

            ## Execute insert of data into database
            self.connection.commit()

        
        return item
    
    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.cur.close()
        self.connection.close()
