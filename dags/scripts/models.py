from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql.functions import now
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ConsumptionData(Base):
    __tablename__ = 'tr_electricity_consumption'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(DateTime)
    consumption = Column(Float)
    CreationTime = Column(DateTime(), server_default=now())

    def __repr__(self):
        return f"<ConsumptionData(date={self.date}, consumption={self.consumption})>"


class PriceData(Base):
    __tablename__ = 'tr_electricity_price'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(DateTime)
    price = Column(Float)
    priceEur = Column(Float)
    priceUsd = Column(Float)
    CreationTime = Column(DateTime(), server_default=now())

    def __repr__(self):
        return f"<PriceData(date={self.date}, price={self.price})>"


class PredictionScenario(Base):
    __tablename__ = 'prediction_scenario'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    modelName = Column(String(50))
    description = Column(String(100))
    CreationTime = Column(DateTime(), server_default=now())

    def __repr__(self):
        return f"<PredictionScenario(model_name={self.model_name}, description={self.description})>"


class PredictionResult(Base):
    __tablename__ = 'prediction_result'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    predictionScenarioId = Column(Integer)
    date = Column(DateTime)
    price = Column(Float)
    CreationTime = Column(DateTime(), server_default=now())

    def __repr__(self):
        return f"<PredictionResult(predictionScenarioId={self.predictionScenarioId}, date={self.date}, price={self.price})>"
