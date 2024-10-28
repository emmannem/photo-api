# services/base_service.py
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import TypeVar, Generic, List, Optional, Type
from pydantic import BaseModel

# Definir un genérico para los modelos y esquemas
ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Inicializar el servicio base con el modelo correspondiente.
        :param model: El modelo de SQLAlchemy al que pertenece este servicio
        """
        self.model = model

    def get_all(self, db: Session) -> List[ModelType]:
        """
        Obtener todos los registros del modelo.
        :param db: Sesión de la base de datos.
        :return: Lista de todos los registros.
        """
        return db.query(self.model).all()

    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """
        Obtener un registro por su ID.
        :param db: Sesión de la base de datos.
        :param id: ID del registro.
        :return: Registro si existe, de lo contrario None.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, obj_in: SchemaType) -> ModelType:
        """
        Crear un nuevo registro.
        :param db: Sesión de la base de datos.
        :param obj_in: Esquema con los datos de entrada.
        :return: El nuevo registro creado.
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: SchemaType) -> ModelType:
        """
        Actualizar un registro existente.
        :param db: Sesión de la base de datos.
        :param db_obj: El registro de la base de datos que será actualizado.
        :param obj_in: Esquema con los datos actualizados.
        :return: El registro actualizado.
        """
        obj_data = obj_in.dict(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        """
        Eliminar un registro por su ID.
        :param db: Sesión de la base de datos.
        :param id: ID del registro.
        :return: El registro eliminado, si existe, de lo contrario None.
        """
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj
