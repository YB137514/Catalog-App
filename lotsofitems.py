#!/usr/local/bin/python
# coding: latin-1
import os
import sys


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_schema import Category, Base, Item, User, Pictures

engine = create_engine('sqlite:///catalogwithusers.db')
# Delete database, so that we can populate new entries
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Default", email="example@gmail.com",
             picture='')
session.add(User1)
session.commit()

# Order No 1-- Testudines (turtles)
category1 = Category(user_id=1, name="Testudines (turtles)")
session.add(category1)
session.commit()

# Family No 1--Chelydridae (snapping turtles)
Item1 = Item(
    user_id=1,
    name="Chelydridae (snapping turtles)",
    description='''The Chelydridae are a family of turtles which has seven
     extinct and two extant genera. The extant genera are Chelydra,
      the snapping turtles, and Macrochelys. Both are endemic to the Western
       Hemisphere. The extinct genera are Acherontemys, Chelydrops,
        Chelydropsis, Emarginachelys, Macrocephalochelys, Planiplastron, and
         Protochelydra.''',
    category=category1)
session.add(Item1)
session.commit()


# Pictures of Chelydridae (snapping turtles)

# Alligator snapping turtle (Macrochelys temminckii)
Pic1 = Pictures(
    item=Item1,
    picture='static/uploads/Alligator_snapping_turtle.jpg')
session.add(Pic1)
session.commit()

# Family No 2-- Kinosternidae (mud turtles and musk turtles)

Item2 = Item(
    user_id=1,
    name="Kinosternidae (mud turtles and musk turtles)",
    description='''The Kinosternidae are a family of mostly small turtles
     that includes the mud turtles and musk turtles. The family contains 25
      species within four genera, but taxonomic reclassification is an ongoing
       process, so many sources vary on the exact numbers of species and
        subspecies. They inhabit slow-moving bodies of water, often with soft,
         muddy bottoms and abundant vegetation.''',
    category=category1)

session.add(Item2)
session.commit()

# Pictures of Kinosternidae (mud turtles and musk turtles)

# Flattened musk turtle (Sternotherus depressus)
Pic1 = Pictures(
    item=Item2,
    picture='static/uploads/Sternotherus_depressus.jpg')
session.add(Pic1)
session.commit()

# Family No 3--Emydidae (pond turtles)
Item3 = Item(
    user_id=1,
    name="Emydidae (pond turtles)",
    description='''The Emydidae, commonly called the pond turtles or marsh
     turtles, are a family of turtles.Previously, several species of Asian box
      turtles were classified in the family. However, revised taxonomy has
       separated them to a different family. Now, the Emydidae, with the
       exception of two species of pond turtles, are entirely a Western
       Hemisphere family. The family Emydidae includes close to 50 species
        in 10 genera.''',
    category=category1)

session.add(Item3)
session.commit()

# Pictures of Emydidae (pond turtles)

# Spotted turtle (Clemmys guttata)
Pic1 = Pictures(
    item=Item3,
    picture='static/uploads/1024px-Spotted_Turtle_-_Clemmys_guttata.jpg')
session.add(Pic1)
session.commit()

# Bog turtle (Glyptemys muhlenbergii)
Pic2 = Pictures(item=Item3, picture='static/uploads/Bog_Turtle.jpg')
session.add(Pic2)
session.commit()

# Wood turtle (Glyptemys insculpta)
Pic3 = Pictures(item=Item3, picture='static/uploads/1024px-WoodTurtle.jpg')
session.add(Pic3)
session.commit()

# Common box turtle (Terrapene carolina)
Pic4 = Pictures(
    item=Item3,
    picture='static/uploads/1024px-Florida_Box_Turtle_Digon3a.jpg')
session.add(Pic4)
session.commit()

# Blanding's turtle (Emys blandingii)
Pic5 = Pictures(
    item=Item3,
    picture='static/uploads/Blandings-road-800x600.jpg')
session.add(Pic5)
session.commit()

# Western pond turtle (Actinemys marmorata)
Pic6 = Pictures(
    item=Item3,
    picture='static/uploads/2009-Western-pond-turtle.jpg')
session.add(Pic6)
session.commit()


# Family No 4-- Cheloniidae (sea turtles)
Item4 = Item(
    user_id=1,
    name="Cheloniidae (sea turtles)",
    description='''The Cheloniidae are a family of sea turtles belonging to
     the sea turtle superfamily Chelonioidea.''',
    category=category1)

session.add(Item4)
session.commit()

# Pictures of Cheloniidae (sea turtles)

# Loggerhead sea turtle (Caretta caretta)
Pic1 = Pictures(
    item=Item4,
    picture='static/uploads/1024px-Loggerhead_sea_turtle.jpg')
session.add(Pic1)
session.commit()

# Green sea turtle (Chelonia mydas)
Pic2 = Pictures(
    item=Item4,
    picture='static/uploads/1024px-Green_turtle_swimming_over_coral_reefs_in_Kona.jpg')
session.add(Pic2)
session.commit()

# Hawksbill sea turtle (Eretmochelys imbricata)
Pic3 = Pictures(
    item=Item4,
    picture='static/uploads/1024px-Hawksbill_turtle_off_the_coast_of_Saba.jpg')
session.add(Pic3)
session.commit()

# Kemp's ridley sea turtle (Lepidochelys kempii)
Pic4 = Pictures(
    item=Item4,
    picture='static/uploads/1024px-Lepidochelys_kempii.jpg')
session.add(Pic4)
session.commit()

# Olive ridley sea turtle (Lepidochelys olivacea)
Pic5 = Pictures(
    item=Item4,
    picture='static/uploads/Turtle_golfina_escobilla_oaxaca_mexico_claudio_giovenzana_2010.jpg')
session.add(Pic5)
session.commit()


# Order No 2-- Squamata (scaled reptiles)
category2 = Category(user_id=1, name="Squamata (scaled reptiles)")

session.add(category2)
session.commit()

# Family No 1--Crotaphytidae (collared lizards)
Item1 = Item(
    user_id=1,
    name="Crotaphytidae (collared lizards)",
    description='''The Crotaphytidae, or collared lizards, are a family of
     desert-dwelling reptiles native to the Southwestern United States and
      northern Mexico. They are very fast-moving animals, with long limbs and
      tails, and are carnivorous, feeding mainly on insects and smaller
       lizards.''',
    category=category2)

session.add(Item1)
session.commit()

# Pictures of Crotaphytidae (collared lizards)

# Blunt-nosed leopard lizard (Gambelia sila)
Pic1 = Pictures(item=Item1, picture='static/uploads/Gambelia_silus.gif')
session.add(Pic1)
session.commit()

# Family No 2--Phrynosomatidae (horned lizards and spiny lizards)
Item2 = Item(
    user_id=1,
    name="Phrynosomatidae (horned lizards and spiny lizards)",
    description='''The Phrynosomatidae are a diverse family of lizards,found
     from Panama to the extreme south of Canada. Many members of the group are
      adapted to life in hot, sandy deserts, although the spiny lizards prefer
       rocky deserts or even relatively moist forest edges, and the
        short-horned lizard lives in prairie or sagebrush environments.
         The group includes both egg-laying and viviparous species, with the
          latter being more common in species living at high elevations''',
    category=category2)

session.add(Item2)
session.commit()

# Pictures of Phrynosomatidae (horned lizards and spiny lizards)

# Dunes sagebrush lizard (Sceloporus arenicolus)
Pic1 = Pictures(item=Item2, picture='static/uploads/sand_dune_lizard.jpg')
session.add(Pic1)
session.commit()

# Coachella Valley fringe-toed lizard
Pic2 = Pictures(
    item=Item2,
    picture='static/uploads/Coachella_Valley_Fringe-toed_Lizard.JPG')
session.add(Pic2)
session.commit()

# Family No 3--Colubridae (colubrid snakes)

Item3 = Item(
    user_id=1,
    name="Colubridae (colubrid snakes)",
    description='''The Colubridae (from Latin coluber, snake) are a family of
     snakes. With 304 genera and 1,938 species, Colubridae is the largest
      snake family, and includes about two-thirds of all living snake species.
       The earliest species of the family date back to the Oligocene epoch.
        Colubrid species are found on every continent except Antarctica''',
    category=category2)

session.add(Item3)
session.commit()

# Pictures of Family No 3--Colubridae (colubrid snakes)

# Southern hog-nosed snake (Heterodon simus)
Pic1 = Pictures(item=Item3, picture='static/uploads/Florida_red.jpg')
session.add(Pic1)
session.commit()

# Louisiana pine snake (Pituophis ruthveni)
Pic2 = Pictures(
    item=Item3,
    picture='static/uploads/PinesnakeSaenz_nr-page.jpg')
session.add(Pic2)
session.commit()

# Rim rock crown snake (Tantilla oolitica)
Pic3 = Pictures(item=Item3, picture='static/uploads/Rim_rock.jpg')
session.add(Pic3)
session.commit()

# Giant garter snake (Thamnophis gigas)
Pic4 = Pictures(
    item=Item3,
    picture='static/uploads/1024px-Giant_Garter_Snake_1.jpg')
session.add(Pic4)
session.commit()


# Family No 4--  Pythonidae (pythons)

Item4 = Item(
    user_id=1,
    name=" Pythonidae (pythons)",
    description='''The Pythonidae, commonly known simply as pythons are a
     family of nonvenomous snakes found in Africa, Asia, and Australia. Among
      its members are some of the largest snakes in the world. Eight genera
       and 26 species are currently recognized''',
    category=category2)

session.add(Item4)
session.commit()

# Pictures of Family No 4-- Pythonidae (pythons)

# Indian Python (Python molurus)
Pic1 = Pictures(
    item=Item4,
    picture='static/uploads/1024px-Labial_Pits_of_P_molorus.JPG')
session.add(Pic1)
session.commit()


#  Order No 3-- Caudata (salamanders)
category3 = Category(user_id=1, name="Caudata (salamanders)")
session.add(category3)
session.commit()

# Family No 1--Ambystomatidae (mole salamanders)
Item1 = Item(
    user_id=1,
    name="Ambystomatidae (mole salamanders)",
    description='''The mole salamanders (genus Ambystoma) are a group of
     salamanders endemic to North America, the only genus in the family
      Ambystomatidae. The group has become famous due to the presence of the
       axolotl (A. mexicanum), widely used in research, and the tiger
        salamander (A. tigrinum, A. mavortium) which is the official
         amphibian of many states, and often sold as a pet.''',
    category=category3)
session.add(Item1)
session.commit()

# Pictures of Family No 1--Ambystomatidae (mole salamanders)

# Reticulated flatwoods salamander(Ambystoma bishopi)
Pic1 = Pictures(
    item=Item1,
    picture='static/uploads/330px-SpottedSalamander.jpg')
session.add(Pic1)
session.commit()

# California tiger salamander(Ambystoma californiense)
Pic2 = Pictures(
    item=Item1,
    picture='static/uploads/California_Tiger_Salamander.jpg')
session.add(Pic2)
session.commit()

# Frosted flatwoods salamander (Ambystoma cingulatum)
Pic3 = Pictures(
    item=Item1,
    picture='static/uploads/Ambystoma_cingulatum_USGS.jpg')
session.add(Pic3)
session.commit()

# Family No 2--Plethodontidae (lungless salamanders)
Item2 = Item(
    user_id=1,
    name="Plethodontidae (lungless salamanders)",
    description='''The Plethodontidae, or lungless salamanders, are a family of
     salamanders. Most species are native to the Western Hemisphere, from
      British Columbia to Brazil, although a few species are found in
       Sardinia, Europe south of the Alps, and South Korea. In terms of number
        of species, they are by far the largest group of salamanders''',
    category=category3)
session.add(Item2)
session.commit()

# Pictures for Family No 2--Plethodontidae (lungless salamanders)

# Red Hills salamander (Phaeognathus hubrichti)
Pic1 = Pictures(
    item=Item2,
    picture='static/uploads/Phaeognathus_hubrichii.jpg')
session.add(Pic1)
session.commit()

# Shenandoah salamander (Plethodon shenandoah)
Pic2 = Pictures(
    item=Item2,
    picture='static/uploads/800px-Shenandoah_Salamander_03.jpg')
session.add(Pic2)
session.commit()


# Jollyville Plateau salamander (Eurycea tonkawae)
Pic3 = Pictures(
    item=Item2,
    picture='static/uploads/Eurycea_tonkawae_IMG_3631.jpg')
session.add(Pic3)
session.commit()

# Texas blind salamander (Eurycea rathbuni)
Pic4 = Pictures(
    item=Item2,
    picture='static/uploads/Texas_blind_salamander.jpg')
session.add(Pic4)
session.commit()


##########


# Order No 4-- Anura (frogs)
category4 = Category(user_id=1, name="Anura (frogs)")
session.add(category4)
session.commit()

# Family No 1--Family Bufonidae (toads)
Item1 = Item(
    user_id=1,
    name="Family Bufonidae (toads)",
    description='''The true toads are the family Bufonidae, members of the order
     Anura (frogs and toads). They are the only family of anurans in which all
      members are known as "toads", although some may be called frogs (such as
       harlequin frogs). The bufonids now comprise more than 35 genera, Bufo
        being the most widespread and well known.''',
    category=category4)
session.add(Item1)
session.commit()


# Pictures of Family No 1--Family Bufonidae (toads)

# Yosemite toad (Anaxyrus canorus)
Pic1 = Pictures(item=Item1, picture='static/uploads/Anaxyrus_canorus.jpg')
session.add(Pic1)
session.commit()

# Black toad (Anaxyrus exsul)
Pic2 = Pictures(item=Item1, picture='static/uploads/Anaxyrus_exsul_001.jpg')
session.add(Pic2)
session.commit()

# Houston toad (Anaxyrus houstonensis)
Pic3 = Pictures(item=Item1, picture='static/uploads/1024px-Houston_toad.jpg')
session.add(Pic3)
session.commit()

# Amargosa toad (Anaxyrus nelsoni)
Pic4 = Pictures(
    item=Item1,
    picture='static/uploads/1024px-Anaxyrus_nelsoni.jpg')
session.add(Pic4)
session.commit()

# Family No 2-- Family Ranidae (true frogs)

Item2 = Item(
    user_id=1,
    name="Family Ranidae (true frogs)",
    description='''The true frogs, family Ranidae, have the widest
     distribution of any frog family.''',
    category=category4)

session.add(Item2)
session.commit()

# Pictures of Family No 2-- Family Ranidae (true frogs)

# Chiricahua leopard frog (Rana chiricahuensis)
Pic1 = Pictures(
    item=Item2,
    picture='static/uploads/Chiricahua_leopard_frog_01.jpg')
session.add(Pic1)
session.commit()

# Tarahumara frog (Rana tarahumarae)
Pic2 = Pictures(item=Item2, picture='static/uploads/Rana_tarahumarae.jpg')
session.add(Pic2)
session.commit()

# California red-legged frog (Rana draytonii)
Pic3 = Pictures(item=Item2, picture='static/uploads/Rana_aurora.jpg')
session.add(Pic3)
session.commit()


##########

# Order No 5-- Sirenia (sea cows)
category5 = Category(user_id=1, name="Sirenia (sea cows)")
session.add(category5)
session.commit()

# Family No 1--Trichechidae (manatees)
Item1 = Item(
    user_id=1,
    name="Trichechidae (manatees)",
    description='''Manatees (family Trichechidae, genus Trichechus) are large,
     fully aquatic, mostly herbivorous marine mammals sometimes known as sea
      cows. There are three accepted living species of Trichechidae,
       representing three of the four living species in the order Sirenia:
        the Amazonian manatee (Trichechus inunguis), the West Indian manatee
         (Trichechus manatus), and the West African manatee (Trichechus
          senegalensis). They measure up to 13 feet (4.0 m) long, weigh as
           much as 1,300 pounds (590 kg) and have paddle-like flippers.''',
    category=category5)
session.add(Item1)
session.commit()


# Pictures of Family No 1--Trichechidae (manatees)

# West Indian manatee (Trichechus manatus)
Pic1 = Pictures(
    item=Item1,
    picture='static/uploads/1024px-Manatee_with_calf.PD_-_colour_corrected.jpg')
session.add(Pic1)
session.commit()
##########################

# Order No 6-- Rodentia (rodents)
category6 = Category(user_id=1, name="Rodentia (rodents)")
session.add(category6)
session.commit()

# Family No 1--Sciuridae (squirrels)
Item1 = Item(
    user_id=1,
    name="Sciuridae (squirrels)",
    description='''Squirrels are members of the family Sciuridae, consisting
     of small or medium-size rodents. The family includes tree squirrels,
      ground squirrels, chipmunks, marmots (including woodchucks), flying
       squirrels, and prairie dogs. Squirrels are indigenous to the Americas,
        Eurasia, and Africa, and have been introduced to Australia.
         The earliest known squirrels date from the Eocene and are most
          closely related to the mountain beaver and to the dormouse among
           living rodent families.''',
    category=category6)
session.add(Item1)
session.commit()


# Pictures of Family No 1--Sciuridae (squirrels)

# Utah prairie dog (Cynomys parvidens)
Pic1 = Pictures(item=Item1, picture='static/uploads/Utah.jpg')
session.add(Pic1)
session.commit()

# Idaho ground squirrel (Urocitellus brunneus)
Pic2 = Pictures(item=Item1, picture='static/uploads/Gs5.jpg')
session.add(Pic2)
session.commit()

# San Joaquin antelope squirrel (Ammospermophilus nelsoni)
Pic2 = Pictures(
    item=Item1,
    picture='static/uploads/Lokerngzpj.Par.2b3ba23d.Image.298.272.jpg')
session.add(Pic2)
session.commit()

# Family No 2-- Heteromyidae (kangaroo rats, kangaroo mice, and pocket mice)

Item2 = Item(
    user_id=1,
    name="Heteromyidae (kangaroo rats, kangaroo mice, and pocket mice)",
    description='''Heteromyidae is a family of rodents comprised by kangaroo
     rats, kangaroo mice, and pocket mice. Most heteromyids live in complex
      burrows within the deserts and grasslands of western North America,
       though species within the genera Heteromys and Liomys are also found in
        forests and their range extends down as far as northern South America.
         They feed mostly on seeds and other plant parts, which they carry in
          their fur-lined cheek pouches to their burrows.''',
    category=category6)

session.add(Item2)
session.commit()

# Pictures of Heteromyidae (kangaroo rats, kangaroo mice, and pocket mice)

# Giant kangaroo rat (Dipodomys ingens)
Pic1 = Pictures(
    item=Item2,
    picture='static/uploads/1024px-Dipodomys_ingens.jpg')
session.add(Pic1)
session.commit()

# Fresno kangaroo rat (Dipodomys nitratoides)
Pic2 = Pictures(
    item=Item2,
    picture='static/uploads/1024px-Dipodomys_nitratoides.jpg')
session.add(Pic2)
session.commit()

# Family No 3--Cricetidae (New World rats and mice)
Item3 = Item(
    user_id=1,
    name="Cricetidae (New World rats and mice)",
    description='''The Cricetidae are a family of rodents in the large and
     complex superfamily Muroidea. It includes true hamsters, voles, lemmings,
      and New World rats and mice. At almost 600 species, it is the
       second-largest family of mammals, and has members throughout the New
        World, Asia, and Europe.''',
    category=category6)

session.add(Item3)
session.commit()

# Pictures of Family No 3--Cricetidae (New World rats and mice)

# Salt marsh harvest mouse (Reithrodontomys raviventris)
Pic1 = Pictures(
    item=Item3,
    picture='static/uploads/Reithrodontomys_raviventris.jpg')
session.add(Pic1)
session.commit()

#######

# Order No 7-- Lagomorpha (hares, rabbits, and pikas)
category7 = Category(user_id=1, name="Lagomorpha (hares, rabbits, and pikas)")

session.add(category7)
session.commit()

# Family No 1--Leporidae (hares and rabbits)
Item1 = Item(
    user_id=1,
    name="Leporidae (hares and rabbits)",
    description='''The Leporidae are a family of mammals that include rabbits
     and hares, over 60 species in all. The Latin word Leporidae means "those
      that resemble lepus" (hare). Together with the pikas, the Leporidae
       constitute the mammalian order Lagomorpha. Leporidae differ from pikas
        in that they have short, furry tails and elongated ears and hind
         legs.''',
    category=category7)

session.add(Item1)
session.commit()

# Pictures of Family No 1--Leporidae (hares and rabbits)

# New England cottontail (Sylvilagus transitionalis)
Pic1 = Pictures(
    item=Item1,
    picture='static/uploads/1024px-New_England_cottontail.jpg')
session.add(Pic1)
session.commit()

########################


# Order No 8--  Soricomorpha (shrews, moles, and relatives)
category8 = Category(
    user_id=1,
    name="Soricomorpha (shrews, moles, and relatives)")
session.add(category8)
session.commit()

# Family No 1--Soricidae (shrews)
Item1 = Item(
    user_id=1,
    name="Soricidae (shrews)",
    description='''Shrew or shrew mouse (family Soricidae) is a small mole-
    like mammal classified in the order Soricomorpha. True shrews are also not
     to be confused with West Indies shrews, treeshrews, otter shrews, or
     elephant shrews, which belong to different families or orders.''',
    category=category8)
session.add(Item1)
session.commit()


# Pictures of Family No 1--Soricidae (shrews)

# Pribilof Island shrew (Sorex pribilofensis)
Pic1 = Pictures(
    item=Item1,
    picture='static/uploads/Southern_short-tailed_shrew.jpg')
session.add(Pic1)
session.commit()

###########################

# Order No 9-- Chiroptera (bats)
category9 = Category(user_id=1, name="Chiroptera (bats)")
session.add(category9)
session.commit()

# Family No 1--Phyllostomidae (leaf-nosed bats)
Item1 = Item(
    user_id=1,
    name="Phyllostomidae (leaf-nosed bats)",
    description='''The New World leaf-nosed bats (Phyllostomidae) are found
     throughout Central and South America, from Mexico to northern Argentina.
      They are ecologically the most varied and diverse family within the
       order Chiroptera. Most species are insectivorous, but the phyllostomid
        bats include within their number true predatory species as well as
         frugivores (subfamily Stenodermatinae and Carolliinae).''',
    category=category9)
session.add(Item1)
session.commit()


# Pictures of Phyllostomidae (leaf-nosed bats)

# Greater long-nosed bat (Leptonycteris nivalis)
Pic1 = Pictures(item=Item1, picture='static/uploads/Leptonycteris_nivalis.jpg')
session.add(Pic1)
session.commit()

# Lesser long-nosed bat (Leptonycteris yerbabuenae)
Pic2 = Pictures(item=Item1, picture='static/uploads/Dk8i5oik.jpg')
session.add(Pic2)
session.commit()

# Family No 2-- Vespertilionidae (vesper bats)

Item2 = Item(
    user_id=1,
    name="Vespertilionidae (vesper bats)",
    description='''Vesper bats (family Vespertilionidae), also known as
     evening bats or common bats, are the largest and best-known family of
      bats. They belong to the suborder Microchiroptera (microbats). Over 300
       species are distributed all over the world, on every continent except
        Antarctica. It owes its name to the Latin word vespertilio ("bat"),
         from vesper, meaning "evening".''',
    category=category9)

session.add(Item2)
session.commit()

# Pictures of Vespertilionidae (vesper bats)

# Indiana bat (Myotis sodalis)
Pic1 = Pictures(item=Item2, picture='static/uploads/Indiana_Bat_FWS.jpg')
session.add(Pic1)
session.commit()

# Family No 3--Molossidae (free-tailed bats)
Item3 = Item(
    user_id=1,
    name="Molossidae (free-tailed bats)",
    description='''The Molossidae, or free-tailed bats, are a family of bats
     within the order Chiroptera. They are generally quite robust, and consist
      of many strong flying forms with relatively long and narrow wings.
       Another common name for some members of this group, and indeed a few
        species from other families, is mastiff bat.''',
    category=category9)

session.add(Item3)
session.commit()

# Pictures of Molossidae (free-tailed bats)

# Florida bonneted bat (Eumops floridanus
Pic1 = Pictures(item=Item3, picture='static/uploads/Lasiurus_borealis.jpg')
session.add(Pic1)
session.commit()

###########################


# Order No 10-- Carnivora (dogs, cats, and relatives)
category10 = Category(user_id=1, name="Carnivora (dogs, cats, and relatives)")
session.add(category10)
session.commit()

# Family No 1--Canidae (dogs)
Item1 = Item(
    user_id=1,
    name="Canidae (dogs)",
    description='''The biological family Canidae  is a lineage of carnivorans
     that includes domestic dogs, wolves, foxes, jackals, coyotes, and many
      other extant and extinct dog-like mammals. A member of this family is
       called a canid. The Canidae family is divided into two tribes: the
        Canini (dogs, wolves, jackals, and some South American "foxes") and
         the Vulpini (true foxes).''',
    category=category10)
session.add(Item1)
session.commit()


# Pictures of Family No 1--Canidae (dogs)

# Red wolf (Canis rufus)
Pic1 = Pictures(
    item=Item1,
    picture='static/uploads/1024px-07-03-23RedWolfAlbanyGAChehaw.jpg')
session.add(Pic1)
session.commit()

# Family No 2-- Ursidae (bears)

Item2 = Item(
    user_id=1,
    name="Ursidae (bears)",
    description='''Bears are mammals of the family Ursidae. Bears are classified
     as caniforms, or doglike carnivorans, with the pinnipeds being their
      closest living relatives. Although only eight species of bears are
       extant, they are widespread, appearing in a wide variety of habitats
        throughout the Northern Hemisphere and partially in the Southern
         Hemisphere. Bears are found on the continents of North America, South
          America, Europe, and Asia.''',
    category=category10)

session.add(Item2)
session.commit()

# Pictures of Family No 2-- Ursidae (bears)

# Polar bear (Ursus maritimus)
Pic1 = Pictures(
    item=Item2,
    picture='static/uploads/Polar_Bear_-_Alaska_(cropped).jpg')
session.add(Pic1)
session.commit()

# Family No 3--Mustelidae (weasels and relatives)
Item3 = Item(
    user_id=1,
    name="Mustelidae (weasels and relatives)",
    description='''The Mustelidae (from Latin mustela, weasel) are a family of
     carnivorous mammals, including the otters, badgers, weasel, martens,
      ferrets, minks and wolverines. Mustelids are diverse and the largest
       family in the order Carnivora.''',
    category=category10)

session.add(Item3)
session.commit()

# Pictures of Family No 3--Mustelidae (weasels and relatives)

# Black-footed ferret (Mustela nigripes)
Pic1 = Pictures(item=Item3, picture='static/uploads/Mustela_nigripes_2.jpg')
session.add(Pic1)
session.commit()

# Sea otter (Enhydra lutris)
Pic2 = Pictures(item=Item3, picture='static/uploads/Sea_otter_cropped.jpg')
session.add(Pic2)
session.commit()


# Family No 4-- Otariidae (eared seals)
Item4 = Item(
    user_id=1,
    name="Otariidae (eared seals)",
    description='''An eared seal or otariid or otary is any member of the
     marine mammal family Otariidae, one of three groupings of pinnipeds. They
      comprise 15 extant species in seven genera (another species became
       extinct in the 1950s) and are commonly known either as sea lions or fur
        seals, distinct from true seals (phocids) and the walrus
         (odobenids).''',
    category=category10)

session.add(Item4)
session.commit()

# Pictures of  Family No 4-- Otariidae (eared seals)

# Northern fur seal (Callorhinus ursinus)
Pic1 = Pictures(item=Item4, picture='static/uploads/Northfursealbull.jpg')
session.add(Pic1)
session.commit()


# Family No 5-- Phocidae (earless seals)
Item5 = Item(
    user_id=1,
    name="Phocidae (earless seals)",
    description='''The earless seals or true seals are one of the three main
     groups of mammals within the seal superfamily, Pinnipedia. All true seals
      are members of the family Phocidae. They are sometimes called crawling
       seals to distinguish them from the fur seals and sea lions of the
        family Otariidae. Seals live in the oceans of both hemispheres and,
         with the exception of the more tropical monk seals, are mostly
          confined to polar, subpolar, and temperate climates. The Baikal
           seal is the only seal found exclusively in fresh water.''',
    category=category10)

session.add(Item5)
session.commit()

# Pictures of  Family No 5-- Phocidae (earless seals)

# Hawaiian monk seal (Monachus schauinslandi)
Pic1 = Pictures(
    item=Item5,
    picture='static/uploads/1024px-Monachus_schauinslandi.jpg')
session.add(Pic1)
session.commit()

# Hooded seal (Cystophora cristata)
Pic2 = Pictures(item=Item5, picture='static/uploads/1024px-Klappmuetze_MK.jpg')
session.add(Pic2)
session.commit()


#######
# Order No 11-- Cetacea (whales and dolphins)

category11 = Category(user_id=1, name="Cetacea (whales and dolphins)")
session.add(category11)
session.commit()

# Family No 1--Physeteridae (sperm whale)
Item1 = Item(
    user_id=1,
    name="Physeteridae (sperm whale)",
    description='''Physeteroidea is a superfamily including just three living
     species of whale; the sperm whale, in the genus Physeter, and the pygmy
      sperm whale and dwarf sperm whale, in the genus Kogia.''',
    category=category11)
session.add(Item1)
session.commit()


# Pictures of Physeteridae (sperm whale)

# Sperm whale (Physeter macrocephalus)
Pic1 = Pictures(
    item=Item1,
    picture='static/uploads/1024px-Mother_and_baby_sperm_whale.jpg')
session.add(Pic1)
session.commit()

# Family No 2-- Balaenidae (bowhead and right whales)

Item2 = Item(
    user_id=1,
    name="Balaenidae (bowhead and right whales)",
    description='''Balaenidae is a family of whales of the suborder mysticete
     that contains two living genera. Historically, it is known as the right
      whale family, as it was thought to contain only species of right whales.
       Through most of the 20th Century, however, that became a much-debated
        (and unresolved) topic amongst the scientific community. Finally, in
         the early 2000s, science reached a definitive conclusion: the bowhead
          whale, once commonly known as the Greenland right whale, was not in
           fact a right whale''',
    category=category11)

session.add(Item2)
session.commit()

# Pictures of Balaenidae (bowhead and right whales)

# North Atlantic right whale (Eubalaena glacialis)
Pic1 = Pictures(
    item=Item2,
    picture='static/uploads/1024px-Eubalaena_glacialis_with_calf.jpg')
session.add(Pic1)
session.commit()

# North Pacific right whale (Eubalaena japonica)
Pic2 = Pictures(
    item=Item2,
    picture='static/uploads/Eubalaena_japonica_drawing.jpg')
session.add(Pic2)
session.commit()

# Family No 3--Balaenopteridae (rorquals)
Item3 = Item(
    user_id=1,
    name="Balaenopteridae (rorquals)",
    description='''Rorquals(Balaenopteridae) are the largest group of baleen
     whales, a family with nine extant species in two genera. They include
      what is believed to be the largest animal that has ever lived, the blue
       whale, which can reach 180 tonnes (200 short tons), and the fin whale,
        which reaches 120 tonnes (130 short tons); even the smallest of the
         group, the northern minke whale, reaches 9 tonnes
          (9.9 short tons).''',
    category=category11)

session.add(Item3)
session.commit()

# Pictures of Family No 3--Balaenopteridae (rorquals)

# Blue whale (Balaenoptera musculus)
Pic1 = Pictures(
    item=Item3,
    picture='static/uploads/Anim1754_-_Flickr_-_NOAA_Photo_Library.jpg')
session.add(Pic1)
session.commit()

# Fin whale (Balaenoptera physalus)
Pic2 = Pictures(item=Item3, picture='static/uploads/LMazzuca_Fin_Whale.jpg')
session.add(Pic2)
session.commit()

# Sei whale (Balaenoptera borealis)
Pic3 = Pictures(
    item=Item3,
    picture='static/uploads/Sei_whale_mother_and_calf_Christin_Khan_NOAA.jpg')
session.add(Pic3)
session.commit()

print "Categories with initial items were added successfully"
