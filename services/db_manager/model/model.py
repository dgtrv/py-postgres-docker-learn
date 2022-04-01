from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker


Base = declarative_base()


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
    story = relationship('Story', back_populates='hero', uselist=False, cascade='all, delete')
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
        result.append(f'  Birthday: {self.birthday}\n')
        result.append(f'  Strength: {self.strength}\n')
        result.append(f'  Mottos:\n')
        
        if len(self.mottos) > 0:
            for motto in self.mottos:
                result.append(f'    Motto with id {motto.motto_id}: {motto.motto}\n')
        else:
            result.append('    No mottos available\n')
        
        result.append(f'  Story: {self.story.story}\n')

        result.append('  Interactions as first hero:\n')
        if len(self.interaction_as_hero_1) > 0:
            for interaction in self.interaction_as_hero_1:
                result.append('    ' + str(interaction))
        else:
            result.append('    No interactions available\n')

        result.append('  Interactions as second hero:\n')
        if len(self.interaction_as_hero_2) > 0:
            for interaction in self.interaction_as_hero_2:
                result.append('    ' + str(interaction))
        else:
            result.append('    No interactions available\n')

        return ''.join(result)


class Side(Base):
    __tablename__ = 'sides'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    heroes = relationship('Hero', back_populates='side')


class Motto(Base):
    __tablename__ = 'mottos'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    hero = relationship('Hero', back_populates='mottos', passive_deletes=True)
    motto_id = Column(Integer)
    motto = Column(String(500), nullable=False)
    interaction_as_hero_1_motto = relationship(
        'Interaction',
        backref='hero_1_motto',
        primaryjoin='Motto.id==Interaction.hero_1_motto_id')
    interaction_as_hero_2_motto = relationship(
        'Interaction',
        backref='hero_2_motto',
        primaryjoin='Motto.id==Interaction.hero_2_motto_id')


class Interaction(Base):
    __tablename__ = 'interactions'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_1_id = Column(Integer, ForeignKey('heroes.id', ondelete='SET NULL'))
    hero_1_motto_id = Column(Integer, ForeignKey('mottos.id', ondelete='SET NULL'))
    hero_2_id = Column(Integer, ForeignKey('heroes.id', ondelete='SET NULL'))
    hero_2_motto_id = Column(Integer, ForeignKey('mottos.id', ondelete='SET NULL'))
    winner = Column(Integer)

    def __repr__(self):
        motto_1 = self.hero_1_motto.motto if self.hero_1_motto else ''
        motto_2 = self.hero_2_motto.motto if self.hero_2_motto else ''
        return f'{self.id} | {self.hero_1_id} | {self.hero_1.name} | {motto_1} | {self.hero_2_id} | {self.hero_2.name} | { motto_2} | {self.winner}'

    def __str__(self):
        result = []
        hero_1_name = 'unknown'
        hero_2_name = 'unknown'
        result.append(f'Interaction started (interaction id: {self.id}):\n')
        if self.hero_1:
            hero_1_name = self.hero_1.name
            result.append(f'  In the left corner (first hero): {self.hero_1.name}'\
                 + f'\n    with motto: {self.hero_1_motto.motto}\n')
        else:
            result.append('  First hero is no more\n')
        if self.hero_2:
            hero_2_name = self.hero_2.name
            result.append(f'  In the right corner (second hero): {self.hero_2.name}'\
                + f'\n    with motto: {self.hero_2_motto.motto}\n')
        else:
            result.append('  Second hero is no more\n')
        result.append('  Result: \n')
        match self.winner:
            case 0:
                result.append('    draw\n')
            case 1:
                result.append(f'    {hero_1_name} won!\n')
            case 2:
                result.append(f'    {hero_2_name} won!\n')
        
        return ''.join(result)


class Story(Base):
    __tablename__ = 'stories'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    hero = relationship('Hero', back_populates='story', passive_deletes=True)
    story = Column(String(500), nullable=False)
