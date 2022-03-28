from datetime import datetime
from model import Hero, Motto, Side, Interaction, Story, Base, Session, engine
from sys import argv, exit

def create_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    #Base.metadata.session.commit()

def seed_db():
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
        session.add(Motto(hero_id=3, motto_id=1, motto='Yeah, well, I\'m going to go build my own theme park with blackjack and hookers. In fact, forget the park.'))
        session.add(Motto(hero_id=4, motto_id=1, motto='I am Lrrr, ruler of the planet Omicron Persei 8. You are hereby conquered!'))
        session.add(Motto(hero_id=4, motto_id=2, motto='I am Lrrr, ruler of the planet Omicron Persei 8. May I crash on your couch?'))
        session.add(Motto(hero_id=5, motto_id=1, motto='I demand the ancient ritual of Rrrmrrrmrrrfrrrmrrr or Consequences!'))
        session.add(Motto(hero_id=5, motto_id=2, motto='I am the boss of you!'))
        session.add(Motto(hero_id=6, motto_id=1, motto='Don\'t worry, I won\'t hurt you.'))
        session.add(Story(hero_id=1, story=''))
        session.add(Interaction(hero_1_id=4, hero_2_id=1, hero_1_motto_id=1, hero_2_motto_id=1, winner=1))
        session.commit()

if len(argv) < 2:
    print('No command provided')
    exit(0)

match argv[1]:
    case 'create_db':
        create_db()
    case 'seed_db':
        seed_db()
    case _:
        print('Command not recognized')
        exit()
