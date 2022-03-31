from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# engine = create_engine('postgresql://dgtrv:dgtrv@80.249.146.139:5432/heroes_db')

Base = declarative_base()

# Герои: id, side (сторона, принадлежность), name, birthday, + любые на ваше усмотрение. Минимум 3 героя на каждой стороне. НЕОБЯЗАТЕЛЬНО: числовая сила героя, которая влияет на вероятность победы.
# TODO: reprs
# TODO: 

class Hero(Base):
    __tablename__ = 'heroes'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    side_id = Column(Integer, ForeignKey('sides.id'), nullable=False)
    side = relationship('Side', back_populates='heroes')
    name = Column(String(30), nullable=False)
    birthday = Column(DateTime(timezone=True))
    strength = Column(Integer)
    mottos = relationship('Motto', back_populates='hero', cascade='all, delete')
    story = relationship('Story', back_populates='hero', uselist=False)
    interaction_as_hero_1 = relationship(
        'Interaction',
        backref='hero_1',
        primaryjoin='Hero.id==Interaction.hero_1_id')
    interaction_as_hero_2 = relationship(
        'Interaction',
        backref='hero_2',
        primaryjoin='Hero.id==Interaction.hero_2_id')
    
    def __repr__(self):
        return f'{self.id} | {self.name} | {self.side.name}'

    def __str__(self):
        result = []
        result.append(f'Info for hero named \"{self.name}\" (id = {self.id}) from {self.side.name}:\n')
        result.append(f'Birthday: {self.birthday}\n')
        result.append(f'Strength: {self.strength}\n')
        result.append(f'Mottos:\n')
        
        if len(self.mottos) > 0:
            for motto in self.mottos:
                result.append(f'(Motto with id {motto.motto_id}: {motto.motto}\n')
        else:
            result.append('No mottos available\n')
        
        result.append(f'Story: {self.story.story}\n')

        result.append('Interactions as first hero:\n')
        if len(self.interaction_as_hero_1) > 0:
            for interaction in self.interaction_as_hero_1:
                result.append(str(interaction))
        else:
            result.append('No interactions available\n')

        result.append('Interactions as second hero:\n')
        if len(self.interaction_as_hero_2) > 0:
            for interaction in self.interaction_as_hero_2:
                result.append(str(interaction))
        else:
            result.append('No interactions available\n')

        return ''.join(result)


# Sides
class Side(Base):
    __tablename__ = 'sides'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    heroes = relationship('Hero', back_populates='side')


# Слоганы героев: id, hero_id, moto_id (нумерация у каждого героя с 1), moto (текст слогана). У каждого героя должно быть от 1-го до нескольких слоганов.
class Motto(Base):
    __tablename__ = 'mottos'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    hero = relationship('Hero', back_populates='mottos', passive_deletes=True)
    motto_id = Column(Integer) #(нумерация у каждого героя с 1),
    motto = Column(String(500), nullable=False) #(текст слогана). У каждого героя должно быть от 1-го до нескольких слоганов.
    interaction_as_hero_1_motto = relationship(
        'Interaction',
        backref='hero_1_motto',
        primaryjoin='Motto.id==Interaction.hero_1_motto_id')
    interaction_as_hero_2_motto = relationship(
        'Interaction',
        backref='hero_2_motto',
        primaryjoin='Motto.id==Interaction.hero_2_motto_id')

# Столкновения героев: id, hero_1_id, hero_1_moto_id (= id таблицы слоганов), hero_2_id, hero_2_moto_id, winner (0 для ничьей, 1 для героя 1, 2 для героя 2). Герой 1 - тот, кто инициировал столкновение или напал первый или нанёс первый удар. Если невозможно определить - то случайный герой.
class Interaction(Base):
    __tablename__ = 'interactions'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_1_id = Column(Integer, ForeignKey('heroes.id', ondelete='SET NULL'))
    #hero_1 = relationship('Hero', back_populates='interaction_as_hero_1', primaryjoin=(Hero.id == hero_1_id))
    hero_1_motto_id = Column(Integer, ForeignKey('mottos.id', ondelete='SET NULL')) #(= id таблицы слоганов),
    #mottos_1 = relationship('Motto', back_populates='interactions_as_hero_1_motto', primaryjoin=(Motto.id == hero_1_motto_id))
    hero_2_id = Column(Integer, ForeignKey('heroes.id', ondelete='SET NULL'))
    #hero_2 = relationship('Hero', back_populates='interactions_as_hero_2', primaryjoin=(Hero.id == hero_2_id))
    hero_2_motto_id = Column(Integer, ForeignKey('mottos.id', ondelete='SET NULL'))
    #mottos_2 = relationship('Motto', back_populates='interactions_as_hero_2_motto', primaryjoin=(Motto.id == hero_2_motto_id))
    winner = Column(Integer) #(0 для ничьей, 1 для героя 1, 2 для героя 2)

    def __repr__(self):
        motto_1 = self.hero_1_motto.motto if self.hero_1_motto else ''
        motto_2 = self.hero_2_motto.motto if self.hero_2_motto else ''
        return f'{self.id} | {self.hero_1_id} | {self.hero_1.name} | {motto_1} | {self.hero_2_id} | {self.hero_2.name} | { motto_2} | {self.winner}'

    def __str__(self):
        result = []
        result.append('Interaction started:\n')
        if self.hero_1:
            result.append(f'In the left corner (first hero): {self.hero_1.name}'\
                 + f'\n with motto: {self.hero_1_motto.motto}\n')
        else:
            result.append('First hero is no more\n')
        if self.hero_2:
            result.append(f'In the right corner (second hero): {self.hero_2.name}'\
                + f'\n with motto: {self.hero_2_motto.motto}\n')
        else:
            result.append('Second hero is no more\n')
        result.append('Result: \n')
        match self.winner:
            case 0:
                result.append('draw\n')
            case 1:
                result.append(f'{self.hero_1.name} won!\n')
            case 2:
                result.append(f'{self.hero_2.name} won!\n')
        
        return ''.join(result)


# Краткая предыстория героя без спойлеров: id, hero_id, story. Где 1 герой = строго 1 история.
class Story(Base):
    __tablename__ = 'stories'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    hero = relationship('Hero', back_populates='story')
    story = Column(String(500), nullable=False)

# НЕОБЯЗАТЕЛЬНО: вьюшка со статистиками: measure, value. Строки для measure, строгая очерёдность: всего героев, героев стороны А, героев стороны Б, всего сражений, победителей со стороны А, победителей со стороны Б, всего слоганов, слоганов героев А, слоганов героев Б.

#Base.metadata.create_all(engine)