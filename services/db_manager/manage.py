from datetime import datetime
from model import Hero, Motto, Side, Interaction, Story, Base, Session, engine
from sys import argv, exit
from random import randint
import logging
from logger.common_log import log_manage_py
from logger.interactions_log import log_for_interactions
from os import getenv

log = log_manage_py
filter_for_draws_in_interactions = lambda log_record: log_record.args['result'] != 'draw'
log_for_interactions.addFilter(filter_for_draws_in_interactions)

def create_db():
    log.info('create_db started')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    log.info('create_db finished')

def seed_db():
    log.info('seed_db started')
    with Session() as session:
        session.add(Side(id=1, name='Planet Earth'))
        session.add(Side(id=2, name='Omicron Persei 8'))
        session.add(Hero(id=1, name='Philip J Fry', side_id=1, birthday=datetime(1974, 8, 14), strength=1))
        session.add(Hero(id=2, name='Turanga Leela', side_id=1, birthday=datetime(2975, 7, 29), strength=100))
        session.add(Hero(id=3, name='Bender Bending Rodriguez', side_id=1, strength=10))
        session.add(Hero(id=4, name='Lrrr', side_id=2, strength=10000))
        session.add(Hero(id=5, name='Ndnd', side_id=2, strength=1000000))
        session.add(Hero(id=6, name='Jrrr', side_id=2, strength=1))
        session.add(Motto(hero_id=1, motto_id=1, motto='I may be just a simple delivery boy with no superpowers, so there\'s nothing I can do.'))
        session.add(Motto(hero_id=1, motto_id=2, motto='Ray-blocking power!'))
        session.add(Motto(hero_id=2, motto_id=1, motto='You gotta do what you gotta do'))
        session.add(Motto(hero_id=3, motto_id=1, motto='Bite my shiny metall ass!'))
        session.add(Motto(hero_id=3, motto_id=2, motto='Kill all humans!'))
        session.add(Motto(hero_id=3, motto_id=3, motto='Yeah, well, I\'m going to go build my own theme park with blackjack and hookers. In fact, forget the park.'))
        session.add(Motto(hero_id=4, motto_id=1, motto='I am Lrrr, ruler of the planet Omicron Persei 8. You are hereby conquered!'))
        session.add(Motto(hero_id=4, motto_id=2, motto='I am Lrrr, ruler of the planet Omicron Persei 8. May I crash on your couch?'))
        session.add(Motto(hero_id=5, motto_id=1, motto='I demand the ancient ritual of Rrrmrrrmrrrfrrrmrrr or Consequences!'))
        session.add(Motto(hero_id=5, motto_id=2, motto='I am the boss of you!'))
        session.add(Motto(hero_id=6, motto_id=1, motto='Don\'t worry, I won\'t hurt you.'))
        session.add(Story(hero_id=1, story='Delivery boy from 20th century'))
        session.add(Story(hero_id=2, story='One-eyed girl'))
        session.add(Story(hero_id=3, story='Spanish singer'))
        session.add(Story(hero_id=4, story='Ruler of the planet Omicron Persei 8'))
        session.add(Story(hero_id=5, story='Wife of the ruler of the planet Omicron Persei 8'))
        session.add(Story(hero_id=6, story='Son of the ruler of the planet Omicron Persei 8'))
        session.commit()
    log.info('seed_db finished')

def add_hero(side_id: int, name: str, birthday: datetime, strength: int = 0) -> None:
    log.info(f'trying to add hero with name \"{name}\"')
    hero = Hero(
        side_id=side_id,
        name=name,
        birthday=birthday,
        strength=strength
    )
    with Session() as session:
        session.add(hero)
        session.commit()
    log.info(f'added hero with name \"{name}\"')

def add_motto(hero_name: str, motto_txt: str) -> None:
    log.info(f'trying to add motto for hero \"{hero_name}\", text: \"{motto_txt}\"')
    with Session() as session:
        hero = session.query(Hero).filter(Hero.name == hero_name).first()
        hero_mottos = session.query(Motto).filter(Motto.hero_id == hero.id).all()
        new_motto_id = hero_mottos[-1] + 1
        new_motto = Motto(hero.id, motto_id=new_motto_id, motto=motto_txt)
        session.add(new_motto)
        session.commit()
    log.info(f'added motto for hero \"{hero_name}\", motto_id: {new_motto_id}')

def add_interaction():
    log.info(f'trying to add interaction')
    hero_1_name = ''
    hero_2_name = ''
    winner = randint(0, 2)
    with Session() as session:
        sides = session.query(Side).all()
        side_1 = sides[0]
        side_2 = sides[1]
        heroes_from_side_1 = session.query(Hero).filter(Hero.side_id == side_1.id).all()
        heroes_from_side_2 = session.query(Hero).filter(Hero.side_id == side_2.id).all()
        hero_1 = heroes_from_side_1[randint(0, len(heroes_from_side_1) - 1)]
        hero_2 = heroes_from_side_2[randint(0, len(heroes_from_side_2) - 1)]
        hero_1_name = hero_1.name
        hero_2_name = hero_2.name
        hero_1_mottos = session.query(Motto).filter(Motto.hero_id == hero_1.id).all()
        hero_1_random_motto = hero_1_mottos[randint(0, len(hero_1_mottos) - 1)]
        hero_2_mottos = session.query(Motto).filter(Motto.hero_id == hero_2.id).all()
        hero_2_random_motto = hero_2_mottos[randint(0, len(hero_2_mottos) - 1)]
        new_interaction = Interaction(
            hero_1_id=hero_1.id,
            hero_2_id=hero_2.id,
            hero_1_motto_id=hero_1_random_motto.id,
            hero_2_motto_id=hero_2_random_motto.id,
            winner=winner
        )
        session.add(new_interaction)
        session.commit()
    log.info('added new interaction')
    result = ''
    match winner:
        case 0:
            result = 'draw'
        case 1:
            result = f'{hero_1_name} wins!'
        case 2:
            result = f'{hero_2_name} wins!'
    log_for_interactions.info(
        'the winner has been chosen, more information: ' + \
            'hero 1: %(hero_1_name)s, hero 2: %(hero_2_name)s, result: %(result)s',
        {'hero_1_name': hero_1_name, 'hero_2_name': hero_2_name, 'result': result}
    )

def add_story(hero_name: str, story_txt: str) -> None:
    log.info(f'trying to add story for hero \"{hero_name}\", text: \"{story_txt}\"')
    with Session() as session:
        hero = session.query(Hero).filter(Hero.name == hero_name).first()
        hero_story = session.query(Story).filter(Story.hero_id == hero.id).first()
        if not hero_story:
            log.info(f'hero {hero_name} doesn\'t have a story now, adding new')
            hero_story = Story(hero_id=hero.id, story=story_txt)
            session.add(hero_story)
        hero_story.story = story_txt
        session.commit()
        log.info(f'added story for hero \"{hero_name}\", story_id: {hero_story.id}')

def del_hero(hero_name: str) -> None:
    log.info(f'trying to remove hero \"{hero_name}\"')
    with Session() as session:
        hero = session.query(Hero).filter(Hero.name == hero_name).first()
        session.delete(hero)
        session.commit()
    log.info(f'removed hero \"{hero_name}\", hero_id was: {hero.id}')

def print_hero(hero_name: str) -> None:
    log.info(f'trying to print hero \"{hero_name}\"')
    with Session() as session:
        if hero_name == '':
            heroes = session.query(Hero).all()
            if len(heroes) == 0:
                log.error('No heroes available')
                return
            for hero in heroes:
                print(str(hero))
            log.info(f'printed all available heroes')
        else:
            hero = session.query(Hero).filter(Hero.name == hero_name).first()
            if not hero:
                log.error(f'Hero with name \"{hero_name}\" not found!')
                return
            print(str(hero))
            log.info(f'printed hero \"{hero_name}\", hero_id was: {hero.id}')

def print_mottos(hero_name: str) -> None:
    log.info(f'trying to print mottos for hero \"{hero_name}\"')
    with Session() as session:
        if hero_name == '':
            heroes = session.query(Hero).all()
            if len(heroes) == 0:
                log.error('No heroes available')
                return
            for hero in heroes:
                print(f'Mottos for hero \"{hero.name}\":')
                for motto in hero.mottos:
                    print(str(motto))
            log.info(f'printed mottos for all available heroes')
        else:
            hero = session.query(Hero).filter(Hero.name == hero_name).first()
            if not hero:
                log.error(f'Hero with name \"{hero_name}\" not found!')
                return
            print(f'Mottos for hero \"{hero.name}\":')
            for motto in hero.mottos:
                print(str(motto.motto))
            log.info(f'printed mottos for hero \"{hero_name}\", hero_id was: {hero.id}')       

if len(argv) < 2:
    log.error('No command provided')
    exit(0)

match argv[1]:
    case 'create_db':
        create_db()
    case 'seed_db':
        seed_db()
    case 'add_hero':
        if len(argv) < 4:
            log.error('Not enough aruments provided')
            exit()
        hero_name = argv[2]
        hero_side_id = int(argv[3])
        hero_birthday = None
        hero_strength = None
        if len(argv) > 4:
            year, month, day = argv[4].split('.')
            hero_birthday = datetime(year, month, day)
        if len(argv) > 5:
            hero_strength = int(argv[5])
        add_hero(
            name=hero_name,
            side_id=hero_side_id,
            birthday=hero_birthday,
            strength=hero_strength
        )
    case 'add_motto':
        if len(argv) < 4:
            log.error('Not enough aruments provided')
            exit()
        hero_name = argv[2]
        motto_txt = argv[3]
        add_motto(
            hero_name=hero_name,
            motto_txt=motto_txt
        )
    case 'add_interaction':
        add_interaction()
    case 'add_story':
        if len(argv) < 4:
            log.error('Not enough aruments provided')
            exit()
        hero_name = argv[2]
        story_txt = argv[3]
        add_story(
            hero_name=hero_name,
            story_txt=story_txt
        )
    case 'del_hero':
        if len(argv) < 3:
            log.error('Not enough aruments provided')
            exit()
        hero_name = argv[2]
        del_hero(hero_name=hero_name)
    case 'print_hero':
        hero_name = ''
        if len(argv) > 2:
            hero_name = argv[2]
        print_hero(hero_name=hero_name)
    case 'print_mottos':
        hero_name = ''
        if len(argv) > 2:
            hero_name = argv[2]
        print_mottos(hero_name=hero_name)
    case _:
        log.error('Command not recognized')
        exit()
