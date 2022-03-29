from datetime import datetime
from .model import Hero, Motto, Side, Interaction, Story, Base, Session, engine
from sys import argv, exit
from random import randint

def add_hero(side_id: int, name: str, birthday: datetime, strength: int = 0) -> None:
    hero = Hero(
        side_id=side_id,
        name=name,
        birthday=birthday,
        strength=strength
    )
    with Session() as session:
        session.add(hero)
        session.commit()

def add_motto(hero_name: str, motto_txt: str) -> None:
    with Session() as session:
        hero = session.query(Hero).filter(Hero.name == hero_name).first()
        hero_mottos = session.query(Motto).filter(Motto.hero_id == hero.id)
        new_motto_id = hero_mottos[-1] + 1
        new_motto = Motto(hero.id, motto_id=new_motto_id, motto=motto_txt)
        session.add(new_motto)
        session.commit()

def add_interaction():
    with Session() as session:
        sides = session.query(Side)
        side_1 = sides[0]
        side_2 = sides[1]
        heroes_from_side_1 = session.query(Hero).filter(Hero.side_id == side_1.side_id)
        heroes_from_side_2 = session.query(Hero).filter(Hero.side_id == side_2.side_id)
        hero_1 = heroes_from_side_1[randint(0, len(heroes_from_side_1) - 1)]
        hero_2 = heroes_from_side_2[randint(0, len(heroes_from_side_2) - 1)]
        hero_1_mottos = session.query(Motto).filter(Motto.hero_id == hero_1.id)
        hero_1_random_motto = hero_1_mottos[randint(0, len(hero_1_mottos) - 1)]
        hero_2_mottos = session.query(Motto).filter(Motto.hero_id == hero_2.id)
        hero_2_random_motto = hero_2_mottos[randint(0, len(hero_2_mottos) - 1)]
        winner = randint(0, 2)
        new_interaction = Interaction(
            hero_1_id=hero_1.id,
            hero_2_id=hero_2.id,
            hero_1_motto_id=hero_1_random_motto.id,
            hero_2_motto_id=hero_2_random_motto.id
        )
        session.add()
        session.commit()

def add_story(hero_name: str, story_txt: str) -> None:
    with Session() as session:
        hero = session.query(Hero).filter(Hero.name == hero_name).first()
        hero_story = session.query(Story).filter(Story.hero_id == hero.id).first()
        if not hero_story:
            hero_story = Story(hero_id=hero.id, story=story_txt)
            session.add(hero_story)
        hero_story.story = story_txt
        session.commit()

def del_hero(hero_name: str) -> None:
    with Session() as session:
        hero = session.query(Hero).filter(Hero.name == hero_name).first()
        session.delete(hero)
        session.commit()

if len(argv) < 2:
    print('No command provided')
    exit(0)

match argv[1]:
    case 'add_hero':
        if len(argv) < 4:
            print('Not enough aruments provided')
            exit()
        hero_name = argv[3]
        hero_side_id = int(argv[4])
        hero_birthday = None
        hero_strength = None
        if len(argv) > 4:
            year, month, day = argv[5].split('.')
            hero_birthday = datetime(year, month, day)
        if len(argv) > 5:
            hero_strength = int(argv[6])
        add_hero(
            name=hero_name,
            side_id=hero_side_id,
            birthday=hero_birthday,
            strength=hero_strength
        )
    case 'add_motto':
        if len(argv) < 4:
            print('Not enough aruments provided')
            exit()
        hero_name = argv[3]
        motto_txt = argv[4]
        add_motto(
            hero_name=hero_name,
            motto_txt=motto_txt
        )
    case 'add_interaction':
        add_interaction()
    case 'add_story':
        if len(argv) < 4:
            print('Not enough aruments provided')
            exit()
        hero_name = argv[3]
        story_txt = argv[4]
        add_story(
            hero_name=hero_name,
            story_txt=story_txt
        )
    case 'del_hero':
        if len(argv) < 3:
            print('Not enough aruments provided')
            exit()
        hero_name = argv[3]
        del_hero(hero_name=hero_name)
    case _:
        print('Command not recognized')
        exit()
