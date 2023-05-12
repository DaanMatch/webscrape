# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from dotenv import load_dotenv
import os
import re

#class PhoneValidationPipeline:
#   def process_item(self, item, spider):
#        phone = item['phone_no']
#        if not re.match(r'\d{4}-\d{6}', phone):
#            raise ValueError(f"Invalid phone number: {phone}")
#       return item

#class EmailValidationPipeline:
#    def process_item(self, item, spider):
#       email = item['email']
#        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            # Return the item unchanged if the email format is invalid
#            return item
        # If the email format is valid or no email is provided, return the item
#        return item


class NationaltrustScraperPipeline:

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
            "user"      : 'postgres',
            "password"  : 'Classof2024!'
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
        );
        CREATE TABLE IF NOT EXISTS public.Geography
        (
        Geocode character varying(255),
        Country character varying(255),
        State character varying(255),
        "PIN" character varying(255),
        District character varying(255),
        SubDistrict character varying(255),
        Municipality character varying(255),
        City character varying(255),
        Town character varying(255),
        Block character varying(255),
        Village character varying(255),
        Ward character varying(255)
        );
        """)
    def process_item(self, item, spider):
        # Check to see if text is already in database 
        self.cur.execute("SELECT * FROM NgoContact WHERE ngoName = %s", (item['organization_name'],))
        result = self.cur.fetchone()

        # If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['organization_name'])
        # If ngo isn't in the DB, insert data
        else:
            # Define insert statement
            self.cur.execute(""" insert into NgoContact (ngoName, OrgEmail, OfficePhone, PhysicalAddress, ChairmanName, OrgType) 
                                values (%s,%s,%s,%s,%s,%s)""", (
                item["organization_name"],
                item["email"],
                item["phone_no"],
                item["address"],
                item["authorized_person"],
                item["schemes_enrolled"]
            ))

            self.cur.execute("""INSERT INTO Geography (State, District) 
                            VALUES (%s, %s)""", (
            item["state"],
            item["district"]
            ))
            ## Execute insert of data into database
            self.connection.commit()
        return item
    
    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()