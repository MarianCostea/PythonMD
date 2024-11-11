import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Master(Base):
    __tablename__ = 'masters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    details = relationship("Detail", back_populates="master")

class Detail(Base):
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True)
    master_id = Column(Integer, ForeignKey('masters.id'))
    detail_info = Column(String)
    master = relationship("Master", back_populates="details")
    sub_details = relationship("SubDetail", back_populates="detail")

class SubDetail(Base):
    __tablename__ = 'subdetails'
    id = Column(Integer, primary_key=True)
    detail_id = Column(Integer, ForeignKey('details.id'))
    subdetail_info = Column(String)
    detail = relationship("Detail", back_populates="sub_details")


engine=create_engine('postgresql+psycopg2://pgadmin:[][][]@localhost/demo')
Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()

def insert_data():
    master1 = Master(name="Master1")
    master2 = Master(name="Master2")
    detail1 = Detail(detail_info="Detail1 for Master1", master=master1)
    detail2 = Detail(detail_info="Detail2 for Master1", master=master1)
    detail3 = Detail(detail_info="Detail1 for Master2", master=master2)
    subdetail1 = SubDetail(subdetail_info="SubDetail1 for Detail1", detail=detail1)
    subdetail2 = SubDetail(subdetail_info="SubDetail2 for Detail1", detail=detail1)
    subdetail3 = SubDetail(subdetail_info="SubDetail1 for Detail2", detail=detail2)
    
    session.add_all([master1, master2, detail1, detail2, detail3, subdetail1, subdetail2, subdetail3])
    session.commit()

insert_data()

def query_data():
    masters = session.query(Master).all()
    result = []
    for master in masters:
        master_data = {
            "master": master.name,
            "details": [
                { 
                    "detail_info": detail.detail_info,
                    "sub_details": [
                        subdetail.subdetail_info for subdetail in detail.sub_details
                    ]
                }
                for detail in master.details
            ]
        }
        result.append(master_data)
    return json.dumps(result, indent=2)

json_data = query_data()
print(json_data)