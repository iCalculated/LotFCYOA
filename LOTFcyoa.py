import time as t
import sys
import random as r


def random_events():
    global sundial
    global respect
    global relPiggy
    global estranged
    if day >= 3 and not sundial and r.randint(1, 3) == 1 and tribe <= 3:
        p3("Piggy comes up to you asking if you could build a sundial.")
        p3("He says that it would be useful because you will be able to tell the exact time.")
        p3("However, it could take workers away from the fire and shelters.")
        function_answer = ask("You tell Piggy that...", ["You will work on it today", "You may have a sundial built "
                                                                                      "at some point", "A sundial is "
                                                                                                       "a waste of "
                                                                                                       "time"])
        if function_answer == 0:
            respect += 5
            relPiggy += 10
            p3("Piggy is overjoyed that you are willing to build the sundial.")
            p3("You put as few people on the job as possible, to not divert focus, but it's a simple task anyways.")
            p3("By the end of the day you have a mostly functioning sundial.")
            sundial = True
        if function_answer == 1:
            respect += 3
            relPiggy += 5
            p3("Piggy is somewhat disappointed by the delay, but thanks you for your choice.")
            p3("You put as few people on the job as possible, to not divert focus, but it's a simple task anyways.")
            p3("By the end of the next day you have a mostly functioning sundial.")
            sundial = True
        if function_answer == 2:
            respect += 3
            relPiggy -= 10
            p3("You can see that Piggy is annoyed with your choice, he gets cold, but stays civil.")
            p3("He thanks you for your time and briskly walks away.")
    if day >= 3 and r.randint(1,4) == 1:
        p3("You notice that the stockpile of fruits and other foods is running low.")
        p3("Most of the gatherers are exploring for new groves, as trees are swiftly stripped of fruit.")
        if estranged:
            function_answer = ask("How do you choose to solve the crisis?", ["Demand that food be rationed", "Ignore it"])
        else:
            function_answer = ask("How do you choose to solve the crisis?", ["Demand that food be rationed", "Ignore it", "Send the choir out to find fruit"])
        if function_answer == 0:
            p3("You regretfully order food to be rationed.")
            p3("The crisis is averted, but you can feel anger and hunger simmering.")
            respect -= 5
        elif function_answer == 1:
            if r.randint(1, 4) <= 2:
                p3("The issue resolves itself, new groves being found within a day.")
            else:
                p3("The situation only worsens, and you have to force harsh rations.")
                p3("Everyone complains about being hungry, and tensions are high.")
                if not estranged:
                    p3("Jack says that you have failed the tribe, and splits off with the choir to hunt.")
                    p3("Some littluns go with him, lured by the prospect of food.")
                    estranged = True
        elif function_answer == 2:
            p3("Jack stares daggers at you, but follows your command.")
            if hunting:
                p3("He knows that their hunting has not been very successful.")
            p3("Later, the choir comes back, each member has arms laden with fruit.")


def remove(meeting_item):
    global meetingChoices
    try:
        meetingChoices.remove(meeting_item)
    except ValueError:
        return


def rescue_check():
    spot = 5 * fire_size + 10 * day + 15
    if fire_size == 0:
        spot = 0
    if forestState < 100:
        spot += 5
    if spot >= r.randint(1, 100):
        return True
    else:
        return False


items = ["boat", "leader"]


def event_manager(events):
    global meetingChoices
    global fire_size
    global forestState
    global respectJack
    global respect
    global tribe_count
    global lotf
    global children
    global tribe
    global fire_group

    count = len(events)
    order = r.sample(range(count), count)

    for key in order:
        event = events[key]
        if children <= 1 and alone:
            tribe = 5
        elif children <= 4:
            tribe = 4
        elif tribe_count >= 10:
            tribe = 3
        elif tribe_count > 1:
            tribe = 2
        elif estranged:
            tribe = 1
        else:
            tribe = 0

        if event == "fire":
            if tribe >= 2 and fire_group == "choir":
                fire_group = "none"
            elif tribe >= 4 and fire_group == "littluns":
                fire_group = "none"
            if fire_group == "littluns":
                fire_size += r.randint(-2, 6) - day
                if fire_size < 0:
                        fire_size = 0
            elif fire_group == "choir":
                if tribe < 2:
                    if r.randint(1, 2) == 1:
                        fire_size -= 1
                        if fire_size < 0:
                            fire_size = 0
                else:
                    fire_size -= r.randint(1, 2)
                    if fire_size < 0:
                        fire_size = 0
            else:
                if fire_size <= 5:
                    fire_size = 0
                else:
                    fire_size -= r.randint(2, 4)
                    if fire_size < 0:
                        fire_size = 0

            if fire_size <= 0 and "Relight the fire" not in meetingChoices:
                meetingChoices.append("Relight the fire")

            if fire_size >= 15 and r.randint(1, 100) > 50 and forestState == 100:
                fire_size = 0
                p3("You awaken to the smell of smoke, and as you open your eyes you realize you are witnessing a "
                   "tragedy.")
                p3("Clearly the signal fire has gotten out of control in the night, and the forest nearby is burning.")
                wait()
                p3("Thankfully the burn, while taking out a section of the forest, appears to have spared all of the "
                   "children.")
                p3("But then Piggy exclaims, \"Where is the one with the mark on his face? I can't find him!\"")
                p3("The littluns are in shock, but at Piggy's statement a few begin to tear up as the affects become "
                   "real.")
                if fire_group == "littluns":
                    p3("Sam and Eric come up to you, tearfully saying \"We didn't realize the fire would spread.\"")
                respect -= 20
                children -= 1
                p3("The mood becomes somber, as one of your own is missing, presumably dead.")

        if event == "hunting" and not estranged:

            if day * 10 > r.randint(1, 100):
                respectJack += 15
                p3("Jack and his hunters run into the main clearing, waving spears.")
                if day >= 3:
                    p3("Their faces are all savagely painted.")
                p3("\"We got a pig!\" They are all yelling in celebration.")
                respectJack += 20
                p3("That evening the pig is roasted over the fire, and chunks are distributed.")
                p3("Jack smirks whenever he sees you throughout the evening, especially as the littluns rip into the "
                   "meat passionately.")
            else:
                p3("After a long day of hunting Jack and his choir return.")
                p3("When you ask them how their hunt went Jack mutters under his breath about needing barbed spears.")

        if estranged:
            if day * 10 > r.randint(1, 100) and not tribe == 0:
                p3("The tribe has captured a pig, and started a fire.")
                if tribe == 1 or tribe == 2:
                    p3("Jack invites you to come over, smirking the whole time.")
                    p3("You find people desert you in favor of the more luxurious lifestyle of the tribe.")
                elif tribe == 3:
                    p3("Jack invites you to come over, smirking the whole time.")
                    p3("The remaining littluns run over, already dreaming about the meat they will get.")
                elif tribe >= 4:
                    p3("All you can see is the blaze, and you can hear the festivities.")
                    p3("Piggy, Sam and Eric sit next to you solemnly, seeing how far society has fallen.")
                    if r.randint(1, 100) <= 30 and lotf:
                        p3("A figure appears on the horizon, against the setting sun.")
                        p3("As it comes closer it turns out to be Jack.")
                        p3("He invites you over, to show off everything that used to belong to you.")
                        if ask("Do you go with him?", ["Yes", "No"]) == 0:
                            p3("You follow Jack back to his tribe, once you arrive you can see the enjoyment everyone "
                               "is experiencing.")
                            p3("The festivities are almost getting ritualistic, as the killing of the pig is acted "
                               "out.")
                            p3("All of a sudden, a dirty thing comes out of the forest. The tribe swarms around it "
                               "with spears and rocks.")
                            function_answer = ask("What do you do?", ["Join in", "Run", "Watch"])
                            if function_answer == 0:
                                p3("The mutual lust is too compelling, you grab a rock and jump into the fray.")
                                p3("Everywhere around you there are flailing limbs, but you get a hit at the dirty "
                                   "object.")
                                p3("As it crumples the swarm dissolves, revealing it.")
                                p3("The corpse of Simon.")
                                p3("Bloodied and dirty he looks miserable, and you run away as you still can, "
                                   "your heart pounding in your chest.")
                            elif function_answer == 1:
                                p3("You struggle to tear you eyes away from the incident, an enraged mob tearing the "
                                   "target.")
                                p3("With time it falls apart, all worse for the wear, revealing a corpse.")
                                p3("The corpse of Simon.")
                                p3("Bloodied and dirty he looks miserable, and you run away as you still can, your "
                                   "heart pounding in your chest.")
                            elif function_answer == 2:
                                p3("All you can do is watch in horror, as the swarm tears apart the target.")
                                p3("After the frenzy there are many cuts inflicted by each other in bloodlust, and a "
                                   "corpse is revealed.",
                                   5)
                                p3("The corpse of Simon.")
                                children -= 1
                                p3("Bloodied and dirty he looks miserable, and you run away as you still can, "
                                   "your heart pounding in your chest.")
                            lotf = False
                elif tribe >= 4:
                    p3("You sit on a log, knowing that the tribe is after you.")
                    p3("How did it all go so wrong?")
                    p3("From the hiding spot you can see the brutal festivities, where they savagely reenact the hunt.")
                    p3("You have failed as a leader, but they have failed as humans.")
                    p3("Your interest in this world was waned, and you grab one of the early spears.")
                    p3("You fall on it, feeling a brief moment of sharp pain before eternal darkness.")
                    end()

                desert = r.randint(3, 7)
                children -= desert
                tribe_count += desert

        if event == "boat":
            if r.randint(1, 100) <= 2 * day:
                if rescue_check():
                    p3("A boat appears on the horizon, slowly turning towards the island.")
                    if tribe <= 3:
                        p3("The boat comes ashore, close to the beach on which the plane crashed.")
                        p3("As you step onto it you feel a sense of pride, you have made it.")
                        if tribe >= 1:
                            p3("Though as you take your final steps off the island you weep for those who lost their way.")
                        end()
                else:
                    p3("You can see a boat in the distance, but it fails to notice you.")
                    if fire_size == 0:
                        p3((fire_group, "why is the fire out?"))
                    p3("So close to rescue, yet so far.")
                    respect -= 5


def wait():
    input("Press enter to continue....\n")
    return


def p3(statement, delay=3, disable=False):
    print(statement)
    if not disable:
        t.sleep(delay)


def ask(question, choices):
    # ansCount = len(choices)
    space(1)
    print(question)
    for option in choices:
        print("    ", option)
    answer = input()
    try:
        ret = choices.index(answer)
        return ret
    except ValueError:
        space()
        return ask(question, choices)


def hunt():

    global injury

    p3("\n\nYou have no idea where Piggy, Sam or Eric are, presumably dead or captured.")
    p3("The tribe is after you, Jack has put the final piece in the puzzle of dictatorship.")
    p3("You know they are coming for you.")
    p3("Standing at the edge of the forest, you see the tribe fan out.")
    p3("Their painted faces disguise their identities under the dark clouds")
    p3("The ululating cry rolls across the trees, and you turn to begin your flight.")
    p3("You are filled with a sense of foreboding, nothing good will happen this night.")
    p3("A ululatingi rolls across the trees, and you turn to begin your flight.")
    p3("At your side your spear that used to provide comfort rests,")
    p3("Now as a symbol of everything you worked towards collapsing into savagery.")
    choice = None
    choice = ask("In good health you have a few options, do you head up a tree, into a thicket, or deeper into the forest?", ["Up a tree", "Into the thicket", "Deeper into the forest"])
    if choice == 0:
        tree()
    elif choice == 1:
        thicket()
    elif choice == 2:
        forest()

    p3("You have escaped the first round, but you are still being chased.")
    p3("To further improve your situation the dark clouds release a downpour, with the occasional flash of lightning and boom of thunder.")
    function_answer = ask("Your head is full of yelling, but you find the will to....", ["Head around to the beach", "Run across the island", "Break the line"])
    if function_answer == 0:
        p3("Your path is uncontested, and you manage to run to the beach.")
    elif function_answer == 1:
        p3("Trying to cross the island you are forced up the mountain, your chest heaving with effort.")
        p3("Atop the mountain you are surrounded.")
        p3("Their spears are sharp, fire hardened tips gleaming with rain and certainty.")
        function_answer2 = ask("The ululation continues as the circle closes in, you have only seconds to...", ["Break the line", "Surrender", "Pray"])
        if function_answer2 == 0:
            p3("Not being a hunter, you never knew what the crossbar on a boar spear was for.")
            p3("As your entrails spill out onto the muddy ground you finally understand.")
            end()
        elif function_answer2 == 1:
            p3("There is no longer a reason to live.")
            p3("You have almost left your body before the brutal dismantling begins, hacking with knives and stabbing with spears.")
            p3("As the world fades away you are at peace.")
            end()
        elif function_answer2 == 2:
            if r.randint(1,2) == 1:
                p3("You fall to your knees and pray inches from the spears.")
                p3("A slight tingle comes down your spine, and then you feel nothing as lightning strikes.")
                p3("The bolt smites you into obvlivion before the savages\' eyes.")
            else:
                p3("Your prayers are answered.")
                p3("You had heard stories of island volcanoes, but never expected to see one.")
                p3("The mountain splits around you, shattering the circle as a sea of fire appears beneath you.")
                p3("Your eyes are scorched by the heat as the ground falls beneath you.")
                p3("You are instantly immolated as you meet the shifting lava, along with the savages.")
    elif function_answer == 2:
        p3("As you charge forward the nearest savage blocks you, only to find himself on your spear, right through his chest.")
        p3("His blood spills in a puddle as he falls, indistinguishable from the blood and grime.")
        p3("A second tribesman puts his spear through your arm.")
        if injury:
            p3("The blood loss is too much for you, and you fall onto the first\'s body, now realizing that it's his twin.")
            p3("You lie on the ground, your blood mixing with Sam\'s.")
            p3("Eric's vindicative face obscures your last view of the sky, as he avenges his brother.")
            end()
        else:
            injury = True
        p3("You rip out the spear, as it has no barb, feeling blood run down your arm but not caring.")

    p3("You are close to making it out of the forest.")
    p3("You have some unbased knowledge that if you make it that far you will be free.")
    p3("Darkness is near complete, marred only by lightning strikes that illuminate the mountain as a sleeping behemoth.")
    p3("A sudden flash reveals three figures in front of you.")
    function_answer = ask("The first lowers his spear, what do you do?", ["Charge and stab him", "Deflect his attack", "Jump over him"])
    if function_answer == 0:
        p3("You charge through him with a stab, spear into his left shoulder.")
        p3("He too strkes true, and the blood tells you that you won't make it through the others.")
        p3("He is knocked down, only to be replaced by the next one, who impales your weakened body.")
        end()
    if function_answer == 1:
        p3("You block him, and stab into his woefully small heart. The next one is ready to confront you.")
    if function_answer == 2:
        p3("Your running start downhill allows you to jump over him.")
        p3("You don't entirely clear his figure, stumbling as you catch his head knocking him over.")
        p3("Quickly you stand to prepare for the second.")
    p3("Only two remain between you and salvation. A second strike illuminates your next adversary, and spawns an inferno nearby in the forest.")
    p3("The flames illuminate his snarling face as he pulls back his spear to throw.")
    function_answer = ask("How do you react?", ["Hide behind a tree", "Charge", "Block the spear"])
    if function_answer == 0:
        p3("You feel the heat of the inferno on your back as you throw yourself to the side, but it does not kill you.")
        p3("Ironically, his aim was off, and your movement aligns the spear with the side of your head, killing you instantly.")
        end()
    elif function_answer == 1:
        p3("His spear flies to the side, leaving him vulnerable.")
        p3("As your spear goes through him the fire illuminates his face, one of the boys you never bothered to learned the name of.")
    elif function_answer == 2:
        p3("Miraculously, you knock the spear out of the air.")
        p3("As your spear plunges into his chest you recognize him.")
        p3("One of the boys you never bothered to learn the name of is dying right before you.")
    p3("The boom of thunder provides a perfect crescendo, as you prepare to fight the final savage by the fire.")
    p3("He tentatively raises his spear, clearly larger than the others, something oddly viscous dripping from the tip.")
    function_answer = ask("How do you get around him?", ["Charge", "Run around him", "Throw your spear"])
    if function_answer == 0:
        p3("Jack should have trained his soldiers more.")
        p3("Roger falls lifelessly to the ground, onto the spreading inferno.")
        p3("His blood coats the mud and leaves, and sizzles against the fire.")
        p3("Thunder cuts short the cries of the tribesmen behind you, with flashes of lightning.")
    elif function_answer == 1:
        p3("He is slow to react, and you run past him.")
        p3("Your salvation is here, a ship on the beach.")
        p3("It looms like a hulking collosus, promising escape.")
        p3("A stab of pain shows that the spear has grazed your side, thrown by Roger.")
        p3("The gash burns more than normal and you collapse as you run to the ship.")
        p3("You are recovered by the sailors, but the poison takes your life.")
        end()
    elif function_answer == 2:
        p3("Your spear is perfectly on target, he never sees it coming.")
        p3("It pierces his head, and as you pass you see that you just killed Roger.")

    if r.randint(1,4) == 1:
        p3("You arrive on the beach, devoid of life.")
        p3("As the rain pours the tribe catches up, you yell about the boat but they are consumed by bloodlust as your voice is lost to the storm.")
        p3("Your yelling morphs into screams as they skewer your internal organs.")
        end()
    p3("With the boat in front of you, you have made it.")
    p3("But at what cost?", 10)
    p3("Piggy is dead.")
    p3("Sam and Eric are dead.")
    p3("And at your own hand at that.")
    p3("You have killed children half your age that you never knew the names of.")
    p3("Jack is still around somewhere.")
    p3("The forest is swiftly being consumed by a fire that can fight against the raging storm.")
    p3("So many others have died, or devolved into savagery.", 5)
    p3("You step onto the boat, but your victory is hollow.")
    end()


def tree():
    p3("You choose one of the forest's great trees, but movement draws in the tribe.")
    p3("They surround you, chanting ritualistically. Coming down would mean death.")
    function_answer = ask("What do you do?", ["Swing from a vine like Tarzan", "Jump across to another tree", "Come down"])
    if function_answer == 0:
        chance = r.randint(1,100)
        if chance <= 20:
            p3("As you swing Jack throws a spear through the air, catching you in the center of your back.")
            p3("The shock causes you to release your hold on the vine, and fall to the ground where your body crumples.")
            end()
        elif chance <= 60:
            p3("You gracefully swing into another tree, spears flying by you within reach.")
            p3("Jack's tribe is quick to follow, and you find yourself in the original predicament.")
            tree()
        else:
            p3("You grab a weak vine, and fall to the ground landing on your arm, fracturing it.")
            p3("You try to get up, but the stabbing pain prevents you from doing so.")
            p3("The tribe surrounds you as your body fails on the ground, preparing to have your throat slit as their many pigs.")
            p3("The mob comes witout mercy, jostling you from all directions you are covered in surges of pain until all fades away.")
            end()

def thicket():
    global injury
    p3("In the thicket you are safe, and hidden, until you attempt to leave.")
    p3("The tribe quickly tracks you down, and a boy enters the thicket only for you to stab him, forcing recoil.")
    p3("The savages cry endlessly, a dark and threatening sound.")
    function_answer = ask("When you have no options, what do you do?", ["Climb a tree", "Charge out", "Stay still"])
    if function_answer == 0:
        tree()
    elif function_answer == 2:
        p3("A boulder rolls through your hiding spot, knocking you over.")
        injury = True
        p3("The yelling becomes even louder, and in the chaos you gain a small lead.")
    elif function_answer == 1:
        p3("You catch the guards by surprise, one surprised to see your spear in his chest.")
        p3("Another stabs your side, thankfully with an unbarbed spear.")
        injury = True
        p3("You feel burning pain, but adrenaline allows you to sweep him and keep going.")
        if r.randint(1,2) == 1:
            p3("He was not the only obstacle though")
            p3("You are instantly swarmed, and vivisected by a multitude of spears as all becomes pain.")
            end()
        else:
            p3("Luckily you manage to gain enough ground on the tribe that you can run on, bleeding heavily.")


def forest():
    if r.randint(1, 2) == 1:
        p3("Hunting has honed Jack's aim.")
        p3("You sprint harder than you ever have before, to trip on what seems to be nothing.")
        p3("On the ground you notice the spear through your chest, as the world fades away.")
        end()
    else:
        p3("You escape deeper into the forest, still being followed.")


def troubleshoot():
    print("TROUBLESHOOTING: ", 'firesize ', fire_size, ", fireGroup ", fire_group, ", children ", children, ", tribe ", tribe, ", tribeCount ", tribe_count, ", meetingChoices", meetingChoices, ", items", items)
    return

def end():
    t.sleep(10)
    if mode:
        troubleshoot()
    sys.exit()



def space(count=20):
    for i in range(1, count):
        print("\n")


meetingChoices = []


def meeting(prompt="The lull of conversation dies down, and everyone starts to look towards you. You decide to "
                   "discuss...."):
    global meetingChoices
    global adjourn

    function_answer = meetingChoices[ask(prompt, meetingChoices)]
    if not function_answer == "Adjourning the meeting":
        meetingChoices.remove(function_answer)
    if function_answer == "Relight the fire":
        p3("You and Piggy go to the top of the mountain, and start a new fire with his glasses.")
        fireSize = 15
    if function_answer == "Adjourning the meeting":
        text_choice = r.randint(1,2)
        if text_choice == 1:
            p3("You have to discussed all that you intend to, and the littluns are starting to squirm.")
            p3("You adjourn the meeting, sending everyone off to their tasks.")
        if text_choice == 2:
            p3("The meeting has gone on long enough, and many littluns are clearly getting bored.")
            p3("You adjourn the meeting, sending people to their respective tasks.")
        adjourn = True
    if estranged:
        try:
            remove("Meat")
        except ValueError:
            if mode:
                print("Failed to remove Meat")
            return

    return function_answer


loop = 0
conch = True
bananas = 0


def beach_loop():
    summon = None
    global relPiggy
    global conch
    global loop
    global bananas
    if not loop == 0:
        function_answer = ask("After a period of resting on the beach you find yourself bored, deciding that you "
                              "should...", ["Look for food", "Search for survivors", "Continue to relax on the beach"])
    else:
        function_answer = ask("Standing on the pristine beach you feel the need to take some action in the face of this"
                              " tragedy. Do you...", ["Look for food", "Search for survivors", "Relax on the beach"])
    if function_answer == 0:
        p3("You figure that food will be in the forest, vaguely remembering fruit trees.")
        p3("To your delight you find the trees, laden with bananas, and a squishy, strange olive-grey fruit")
        p3("You can not yet bring yourself to try the strange fruit, but the bananas are tempting, and you find them "
           "sweet.")

        bananas += r.randint(5, 15)

        p3(("You save " + str(bananas) + " bananas for later."), 5)
        p3("You are surprised to see younger children, gorging themselves on all kinds of fruit, clearly not as "
           "cautious as you.")
        wait()
        return beach_loop()
    elif function_answer == 1:
        p3("You decide that searching for other survivors is the most logical choice for you, and after a few minutes"
           " of searching you stumble upon another kid.")
        p3("He wears glasses and is very overweight but seems to be very smart. He says that people call him Piggy.")
        p3("Your search takes you and Piggy to the beach, where a white shape in the water catches Piggy's eye.")
        p3("Carefully tugging it out of the sand, you find it to be a large white shell that Piggy calls a conch.", 5)
        p3("Piggy says that the conch is very valuable and can be blown to produce a tremendous sound.")
        wait()
        summon = "blow"
        conch_choice = ask("What do you do with the conch?", ["Hold", "Discard", "Blow"])
        if conch_choice == 1:
            p3("You are about to throw the conch back into the water, but then Piggy grabs your arm.")
            p3("\"We  might need that later\" he says, and you feel foolish.")
            wait()
            p3("You find yourself putting the horn to your lips and blowing.")
            p3(
                "At first a weak, wavering noise emits from the horn, but as you blow harder it deepens and "
                "strengthens.")
            wait()
            relPiggy = relPiggy - 3
        if conch_choice == 0:
            p3("You find yourself putting the horn to your lips and blowing.")
            p3(
                "At first a weak, wavering noise emits from the horn, but as you blow harder it deepens and "
                "strengthens.")
            wait()
            relPiggy = relPiggy + 3
        if conch_choice == 2:
            p3(
                "At first a weak, wavering noise emits from the horn, but as you blow harder it deepens and "
                "strengthens.")
            wait()
            relPiggy = relPiggy + 5
        conch = True
        relPiggy = relPiggy + 5
    elif function_answer == 2:
        p3("Enjoying the feel of the sun on your face, you decide to lay down and sunbathe on the pristine white sand "
           "of the beach.")
        p3("Exploring the shoreline, you find a large pool that proves to be an ideal swimming pool.")
        wait()
        prob = r.randint(1, 4)
        if prob == 2 or prob == 1:
            p3("As you're swimming in the pool, a rather overweight kid wearing glasses walks up to you, carrying a "
               "large white shell.")
            p3("He says people call him Piggy, and that he found this conch shell which can produce a tremendous sound"
               " when blown.")
            wait()
            relPiggy = relPiggy + 5
            conch = True
            summon = "found"
            ask("He thinks it would be a good idea to gather up the survivors of the plane crash by blowing the shell,"
                " but is having trouble doing it himself...", ["Offer to blow it yourself"])
            p3("At first a weak, wavering noise emits from the horn, but as you blow harder it deepens and strengthens.")
            wait()
        elif prob == 3 or prob == 4:
            loop = loop + 1
            t.sleep(3)
            return beach_loop()
    return summon


p3("\n\n\n\nWelcome to our choose-your-own-adventure-game!")
p3("Created by Sasha Hydrie, Matthias Baese, and Simon Mulrooney.\n\n", 5)

mode = input("Analysis mode? y/N").lower()
if mode == 'y':
    mode = True
    p3("Jack leaving - Over the course of the book, Jack becomes more and more frustrated that he wasn’t picked as leader, and that Ralph is disinterested in meat and only cares about the fire.")
    p3("This leads to the confrontation where he insists that he would be a better chief than Ralph, demanding that ”Whoever wants Ralph not to be chief” (127) to join him.")
    p3("Eventually, Jack’s hatred and jealousy of Ralph leads to him demanding Ralph’s death.\n")
    p3("We chose these beginning questions after carefully analyzing the text, and phrased the first question to match the beginning of the book.")
    p3("For example, at the beginning of the book, Ralph ”Jumped down from the terrace.  The sand was thick over his black shoes” (10).")
    p3("Ralph’s decision to frolic around naked on the beach inspired our option to relax at the beginning. \n")
    p3("Chapter 3: During this chapter the game focuses almost exclusively on the interplay between Ralph and Jack.")
    p3("Now that they both have their own followings, they are on another level of diplomacy than any other characters.")
    p3("At first when Jack asks who wants Ralph not to be chief, \“the silence continued, breathless and heavy and full of shame”(127).")
    p3("He starts off with no followers, as modelled with JF=1. There is a possibility if Ralph does not have enough respect for Jack to start off with a couple of friends, but Jack will likely begin alone.")
    p3("Over time (in the book and in the game) he gathers more followers, which eventually comes to a head with a conflict between the two tribes.")
    p3("In the book this is over Piggy’s glasses, but in the game we made the conflict more devastating and with larger consequences.")
    p3("Throughout the course of this chapter Ralph becomes more and more out of touch, and becomes politically unsuitable even if he is the better leader.")
    p3("This dynamic between the two leaders, with Jack ascending and Ralph descending leads to the inevitable fight, visible when any hegemon is challenged in global politics.")
    p3("Most routes in the game lead this to the hunt. In the game, these two chapters represent the bad options. After Jack leaves, everything disintegrates quite quickly.")
    p3("The three ways to win the game (quickly through the fire, slowly through annihilating Jack and using the fire, or slowly through surviving the hunt) have varying levels of pain along the way, which represents the plot’s descending spiral.\n\n")
if mode == 'n':
    mode = False

p3("You are on a plane, the sky outside stormy, when all of a sudden there is an announcement:")
p3("\"Ladies and gentlemen, this is your captain speaking, we are having some unexpected difficulties.")
p3("As of now we are preparing to make an emergency landing.", 4)
p3("Please do not be alarmed.\"\n", 5)

p3("The plane begins to pitch and roll, fighting to stay stable.", 4)
p3("You can feel the plane quickly losing altitude, and some land appears outside the window.", 4)
p3("The excessive g-force darkens your vision, and you fall unconscious.\n")

wait()

p3("You awake in a tropical forest, torn apart by the plane's \"emergency landing\", still strapped into your chair.")
p3("The sun beats down on you, glistening off the morning dew. You stand up, unstrapping yourself,")
p3(
    "You look out at the seemingly endless ocean. Walking out on the pristine beach the steep curvature of the shoreline is revealed to you.")
p3("The plane must have crashed on a small peninsula. Or... well... lets not jump to conclusions.\n")

wait()

lotf = True
day = 0
respect = 0
respectJack = 0
relPiggy = 0
relJack = 0
conchRule = False
children = r.randint(40, 60)
forestState = 100
fire_size = 0
fire_group = "none"
hunting = False
tribe = 0
tribe_count = 0
estranged = False
sundial = False
alone = False
injury = False

while True:
    # Potentially the gameplay loop

    day = day + 1
    if tribe >= 1:
        estranged = True
    if estranged and tribe == 0:
        tribe = 1

    event_manager(items)
    if mode:
        troubleshoot()
    p3("Day " + str(day))
    if day == 1:
        meetingChoices = ["Learning names", "Building shelters", "Leadership", "A way of getting home",
                          "Adjourning the meeting"]
        method = beach_loop()
        vote = False
        if method == "found" or method == "blow":
            respect = respect + 25
            p3("After a short while, kids begin to filter out of the forest, coming towards the sound of the conch.")
            p3("There are about " + str(
                children) + " kids gathered around you, introducing themselves and chattering quietly about the predicament.")
            wait()
            adjourn = False
            while not adjourn:
                topic = meeting(
                    "Soon the lull of conversation dies down, and the crowd looks to you. You choose to discuss...")
                if topic == "Learning names":
                    p3(
                        "You introduce yourself, before moving around the group in a roughly cyclical matter, with each individual saying their name.")
                    p3(
                        "After learning everyone's names. The ones that stand out to you are Piggy for his intelligence, Jack for his cunning, and Simon for - well....")
                    p3("You can't tell quite what makes Simon stand out.")
                    if r.randint(1, 4) == 2 and not vote:
                        p3("Jack interjects, saying \"We really need to get organized. We should pick a leader.\"")
                        voteQ = ask("How do you reply to Jack?",
                                    ["\"I agree\"", "\"I disagree, why don't we return to more pressing subjects\""])
                        if voteQ == 0:
                            respect += 5
                            p3("\"I agree.\" You reply")
                            topic = "Leadership"
                            meetingChoices.remove("Leadership")
                        if voteQ == 1:
                            respect -= 3
                elif topic == "Building shelters":
                    respect += 5
                    p3("You say \"I assume that everyone wants to have somewhere to sleep at night.\"")
                    relPiggy += 5
                    p3("You order the construction of huts, Piggy swiftly outlining a process to help construct them.")
                if topic == "Leadership" or vote:
                    p3("Jack says, \"I should be our leader. I will have my choir be hunters and we will get some meat!")
                    respectJack += 3
                    p3(
                        "Amid the clamor Roger says \"Let's vote!\" and chaos ensues with chants of \"Vote!\" from the littl\'uns")
                    p3("The crowd seems to be determined, and you realize that you should not resist.")
                    rule = ask(
                        "However, being so out of order prevents any action, so you decide to impose the following rule....",
                        ["All who speak out of turn shall be slaughtered!",
                         "Only 10 people may be at the assembly at a time", "Only he who holds the conch may speak"])
                    if rule == 0:
                        p3("The already crazed mob charges you, crushing you under them.")
                        p3("It seems that you spoke out of turn.")
                        end()
                    elif rule == 2:
                        conchRule = True
                        respect += 30
                        p3("To make yourself heard you blow the conch again.")
                        p3(
                            "The crowd quickly quites, and you explain the rule that you just thought of, including an exception for yourself.")
                    elif rule == 1:
                        p3(
                            "Even as you think it you realize what a terrible idea that is. You don't come up with an alternate solution.")
                    p3("You blow the conch, \"Alright! Let's vote!\"")
                    p3(
                        "\"I guess I will run, who else wishes to run?\" You ask. Jack quickly replies \"I will run as well.\"")
                    if r.randint(1, 3) == 3:
                        p3("Slightly later Piggy nervously volunteers.")
                    voting = r.randint(-10, 10) + respect - respectJack
                    if voting > 1:
                        leader = True
                        p3("A quick show of hands deems you the leader, much to Jack's chagrin.")
                    if voting == 0:
                        p3("Surprisingly Piggy made an impression, and is deemed the leader.")
                    if voting < 1:
                        p3("The crowd favors Jack, and you find yourself more than a little disappointed.")
                elif topic == "A way of getting home":
                    p3("You suggest lighting a signal fire so that ships can see. Many agree, desperate to be rescued.")
                    p3("Piggy suggests putting the fire at the top of the nearby mountain for visibility.")
                    if ask("Do you agree with Piggy?", ["Yes", "No"]) == 0:
                        relPiggy += 5
                    else:
                        relPiggy -= 5
                        p3("Jack disagrees, nodding at Piggy's idea. The argument does not seem worth it.")
                    p3(
                        "The fire is currently a high priority, so progress is made right after the meeting, using Piggy's glasses to start it.")
                    fire_size = 7

        elif method == "hear":
            p3("Attracted by the sound, you and several other kids congregate around the kid holding a conch, who introduces himself as Jack.")
            respectJack = respectJack + 20
        items.append("fire")
        remove("Learning names")
        remove("Leadership")
        remove("Building shelters")
        remove("A way of getting home")
        remove("Building shelters")
        if "fire" in items:
            p3("The journey to the top of the mountain is labor-intensive, but progress is going well.")
            p3("After some logs have been added Piggy says \"We should stop now, we don't want an overly large fire.\"")
            p3(
                "Jack instantly opposes him, almost for the fun of it, \"The bigger the fire, the easier to see\" he counters.")
            decision = ask("You choose to", ["Make the fire larger", "Add a bit to the fire", "Leave it as is"])
            if decision == 0:
                p3("You agree with Jack, piling on more wood.")
                p3("Piggy gets kind of quiet, but continue to follow your lead grudgingly.")
                respectJack += 10
                relPiggy -= 5
                fire_size = 20
            elif decision == 1:
                p3("You look for the in-between option, deciding to add a bit to the fire.")
                p3("Neiter Jack nor Piggy is very happy with that choice.")
                relJack -= 5
                relPiggy -= 5
                fire_size = 10
                if respect < respectJack:
                    p3("When you stop the hunters keep going, saying that it can be a bit larger.")
                    fire_size = 15

            elif decision == 2:
                p3("Piggy is clearly glad that you agree with him, but Jack is staring daggers.")
                p3("He storms off with a few of his hunters, grumbling about hunting.")
                relPiggy += 5
                relJack -= 20
                respect -= 5
    if day == 2:
        meetingChoices.append("Fire management")
        meetingChoices.append("Meat")

        p3("The first day went well, with everyone contributing to improving the situation.")
        p3("Having dealt with a few you now have other issues to bring up at meetings.")
        # print(meetingChoices)
        if ask("Do you want to hold a meeting?", ["Yes", "No"]) == 0:
            respect += 10
            p3("You stand in the middle of the small clearing, bringing the conch up to your lips.")
            p3("Already you are more familiar with blowing the conch, and the deep sound swiftly resonates.")
            if respect > 0:
                p3("From all around kids come running, and within a few minutes the clearing is filled.")
                adjourn = False
                choice = meeting("Just like the last time, the side conversations die down, and everyone begins to look"
                                 " at you. What do you choose to discuss?")
                while not adjourn:

                    if choice == "Fire management":
                        p3("\"If we want to be rescued, we need to keep the fire burning, and that means having some people in charge.\"")
                        if ask("Do you put the choice to vote, or do you choose a group?",
                               ["Vote", "Choose myself"]) == 0:
                            p3("You decide to put the issue to vote.")
                            p3("\"Piggy and I are unable to manage the fire ourselves, we need a designated group, we can either teach the littluns or make it a duty of the choir.\"")
                            p3("However, Jack speaks up, \"My choir has a more important duty, we will hunt for meat. The littluns can manage the fire.\"")
                            if respectJack > 10:
                                respectJack += 3
                                p3(
                                    "You don't feel that it's a good idea to argue with Jack, and he is at least somewhat convincing.")
                                p3(
                                    "You decide that the littluns would be able to manage the fire, at least with a bit of assistance.")
                                fire_group = "littluns"
                            else:
                                if ask("Do you agree with Jack and announce the littluns as the keepers of the fire?",
                                       ["Yes", "No"]) == 0:
                                    relJack += 5
                                    p3("You decree the littluns the keepers of the fire.")
                                    respect -= 3
                                else:
                                    if respect > respectJack:
                                        relJack -= 5
                                        respect += 5
                                        relPiggy += 5
                                        fire_group = "choir"
                                        p3(
                                            "With your higher authority, you decree the choir as the keepers of the fire.")
                                        p3(
                                            "Jack is angry at the decision that you have made, but accepts it, clearly plotting.")
                                    elif respect == respectJack:
                                        relJack -= 10
                                        relPiggy += 5
                                        respect -= 10
                                        p3(
                                            "Neither of you are willing to back down, and the group is split between you.")
                                        fire_group = "none"
                                        p3("You know that you will be unable to manage the fire, but fear retribution.")
                                    elif respectJack > respect:
                                        respect -= 10
                                        relJack += 5
                                        fire_group = "littluns"
                                        p3(
                                            "Jack receives more support from the spectators, and you find yourself powerless to argue.")
                                        p3(
                                            "Jack announces, \"The littluns will manage the fire, as we attend to more important matters.\"")
                        else:
                            decision = ask("Who do you choose to manage the fire?",
                                           ["No one", "The littluns", "The choir"])
                            if decision == 0:
                                fire_group = "none"
                                p3("You announce that the fire should be tended as needed, with no preset group,")
                            if decision == 1:
                                fire_group = "littluns"
                                p3("You deem the littluns the keeper of the fire, receiving some wary looks.")
                            if decision == 2:
                                fire_group = "choir"
                                p3("You deem the choir the keeper of the fire, Jack looking like he is about to protest.")
                    if choice == "Meat":
                        respect += 5
                        p3("You bring up alternate food sources, and instantly Jack jumps in.")
                        p3("\"My choir and I shall hunt the pigs on the island, and bring back meat!\"")
                        if ask("Do you accept Jack's proposition?", ["Yes", "No"]) == 0:
                            relJack += 10
                            respect += 5
                            p3(
                                "You accept Jack's idea without arguing, knowing that it will engage them, even if the fire is more important.")
                            hunting = True
                            fire_group = "littluns"
                        else:
                            relJack -= 5
                            respect += 5
                            p3("You suggest that keeping the fire burning is more important than any hunting.")
                            p3("Jack protests, saying that the others can handle it.")
                            if ask("Do you contest?", ["Yes", "No"]) == 0:
                                relJack -= 10
                                p3(
                                    "As you tell Jack that no one needs meat he storms out, with a few of the choir (and others) following him.")
                                estranged = True
                                tribe = 1
                                remove("Fire management")
                                fire_group = "littluns"
                            else:
                                p3("You agree that the choir can hunt if they really want to.")
                                p3("However, your concession make Jack seem more powerful to the many people around you.")
                                relJack += 5
                                respectJack += 5
                                respect -= 5
                                fire_group = "littluns"

                    if not adjourn:
                        choice = meeting(
                            "The side conversations die down, and everyone looks back to you. What do you choose to discuss?")
    if day == 3:
        p3("As you and the others are discussing various matters, the littluns start chattering fearfully about a beast.")
        p3("You ask incredulously if anyone saw a beast, and a boy with a birthmark mutters something about a giant "
           "snake like creature in the jungle.")
        p3("This is all it takes to convince the littluns, and their terror is obvious.")
        decision = ask("What will you tell them?",
                       ["We will protect you from the beast, if there is one.", "There is no beast, that's ridiculous.",
                        "We will hunt and kill the beast!"])
        if decision == 0:
            p3("You suggest a passive approach, building some fortification.")
            if r.randint(1, 2) == 2:
                p3("Jack insists that you must hunt the beast.")
                p3("He accuses you, \"You are a terrible leader! The beast could attack people while they are away.\"")
                p3("\"I will start my own tribe, that will actually protect you.\" He says to the littluns.")
                estranged = True
                p3("He and his hunters leave the meeting, followed by a few littluns")
                change = r.randint(5, 8)
                tribe_count += change + 10
                children += -1 * change - 10
                respect -= 10
            else:
                p3("Jack and Piggy agree, and the hunters are deemed the guards once the defenses are in place.")
                respect += 5
                p3("After they are completed many littluns are afraid of leaving the camp.")
        elif decision == 1:
            p3("You deny the existence of the beast, calling it simply a bad dream.")
            p3("Jack accuses of you being a terrible leader, \'He won't protect you!\"")
            p3("\"I will start my own tribe, that will actually protect you.\" He says to the littluns.")
            p3("He and the choir walk out, followed by many of the terrified littluns")
            change = r.randint(5, 8)
            tribe_count += change + 10
            children -= change + 10
            respect -= 10
            estranged = True
        elif decision == 2:
            p3("Jack agrees, as Piggy shakes his head.")
            relJack += 5
            respect += 10
            p3(
                "He grabs his spear, and many members of the choir do the same, ready to find whatever scared the littluns.")
            p3("You spend the rest of the day hunting, but are suspicious that it does not exist.")
            p3("When you tell the littluns they are still worried.")
    if day >= 3:
        if r.randint(1, 100) <= day * 10:
            estranged = True
            p3("Jack has been stewing the past few days. He says that the fire is pointless, there will be no rescue.")
            p3("In the morning he announces that he is starting his own tribe, that will be better.")
            tribe = 1
        if tribe <= 3 and estranged and "Attack the tribe" not in meetingChoices:
            meetingChoices.append("Attack the tribe")

        if ask("Do you choose to hold a meeting?", ["Yes", "No"]) == 0:
            adjourn = False
            choice = None
            while not adjourn:
                choice = meeting("As more problems arise you have important things to discuss. You choose to bring up...")
                if choice == "Attack the tribe":
                    adjourn = True
                    p3("Jack is a danger to your society, and as so you order to eliminate him.")
                    p3("You rally your forces, down to even the very last littlun, arming them with spears.")
                    if mode:
                        troubleshoot()
                    if tribe == 1:
                        p3("Your forces charge into Jack's camp at night.")
                        p3("He knows you are coming, but his body is brutally pierced by the flood of littluns all the same.")
                        p3("You want to know that the ends justify the means, but the end is not in sight.")
                        tribe = 0
                        tribe_count = 0
                    elif tribe == 2:
                        battle = r.randint(1,100)
                        p3("You decide that desertion can not be tolerated, Jack and all who follow him must die.")
                        p3("Your victory will make an example to all that doubt you.")
                        if battle < 10:
                            p3("Many find the idea of attacking Jack ridiculous, even the littluns.")
                            p3("Seeing your treachery all but Piggy, Sam and Eric leave you, but even Piggy watches you more closely.")
                        elif battle < 60:
                            p3("In the dead of the night, your forces surround Jack's camp, swiftly pouncing.")
                            p3("The few sleeping forms provide little resistance as all are massacred at your order.")
                            p3("Armed with crude spears and clubs every guard suffers, and Jack's tribe is painfully annhiilated.")
                            p3("You want to know that the ends justify the means, but the end is not in sight.")
                            p3("As you stand among the bodies a single tear drips down your face.")
                            p3("Piggy stands back aghast, yet the littluns celebrate, not knowing the weight of their actions.")
                            tribe = 0
                            tribe_count = 0
                        else:
                            p3("In the dead of the night, your forces surround Jack's camp, ready to pounce.")
                            p3("The older members of your group wait to strike, but the littluns charge in.")
                            p3("Yelling at the top of their lungs lookouts swiftly massacre or capture them.")
                            p3("You try to capitalize on the opportunity, quickly attacking, but all of Jack's forces are alerted.")
                            p3("His fierce posse shred your ill-equipped attacking force.")
                            if r.randint(1,2) == 1:
                                p3("You fight the hardest out of anyone, and Jack personally comes to you, spear in hand.")
                                p3("Hunting has honed his skills, all of a sudden there is a blazing pain in your side as the world goes dark.")
                                p3("You fall to the ground, and the last thing you hear is, \"Say hello the lord of the flies.\"")
                                end()
                            else:
                                p3("You fight harder than anyone, but see your forces fall.")
                                p3("You retreat, running as spears and rocks are hurled at your forces.")
                                p3("Entirely alone, Piggy, Sam and Eric are all gone, dead or presumably captured.")
                                p3("Not even to mention the many others.")
                                p3("You have survived, but you wish you did not, cursing your own foolishness.")
                                children = 1
                                tribe = 5
                    elif tribe == 3:
                        battle = r.randint(1,100)
                        p3("You decide that desertion can not be tolerated, Jack and all who follow him must die.")
                        p3("Your victory will make an example to all that doubt you.")
                        if battle < 20:
                            p3("Many find the idea of attacking Jack ridiculous, and the few littluns in your forces abandon you.")
                            p3("Seeing your treachery all but Piggy, Sam and Eric leave you, but even Piggy watches you more closely.")
                        elif battle < 60:
                            p3("In the dead of the night, your forces surround Jack's camp, swiftly pouncing.")
                            p3("The few sleeping forms provide little resistance as all are massacred at your order.")
                            p3("Armed with crude spears and clubs every guard suffers, and Jack's tribe is painfully annhiilated.")
                            p3("You want to know that the ends justify the means, but but the end is not in sight.")
                            p3("As you stand among the bodies a single tear drips down your face.")
                            p3("So many have died, not only Jack and his choir but also innocents.")
                            p3("Piggy stands back aghast, yet the littluns celebrate, not knowing the weight of their actions.")
                            tribe = 0
                            tribe_count = 0
                        else:
                            p3("In the dead of the night, your forces surround Jack's camp, ready to pounce.")
                            p3("Without older members your group lacks strategy, the littluns charge in.")
                            p3("Yelling at the top of their lungs lookouts swiftly massacre or capture them.")
                            p3("You try to capitalize on the opportunity, quickly attacking, but all of Jack's forces are alerted.")
                            p3("His fierce posse shred your ill-equipped attacking force, as the littluns aligned with him throw stones.")
                            if r.randint(1,3) <= 2:
                                p3("You fight the hardest out of anyone, and Jack personally comes to you, spear in hand.")
                                p3("Hunting has honed his skills, all of a sudden there is a blazing pain in your side as the world goes dark.")
                                p3("You fall to the ground, and the last thing you hear is, \"Say hello the lord of the flies.\"")
                                end()
                            else:
                                p3("You fight harder than anyone, but see your forces fall.")
                                p3("You retreat, running as spears and rocks are hurled at your forces.")
                                p3("Entirely alone, Piggy, Sam and Eric are all gone, dead or presumably captured.")
                                p3("Not even to mention the many others.")
                                p3("You have survived, but you wish you did not, cursing your own foolishness.")
                                children = 1
                                tribe = 5

        if fire_group == "choir" and tribe <= 4:
            p3("Sam and Eric offer to watch the fire now that the choir is gone.")
            if ask("Do you accept?", ["Yes", "No"]) == 0:
                fire_group = "littluns"
                p3("You accept, thankful for the effort but worried about reliability.")
            else:
                fire_group = "none"
                p3("You would rather have no fire than leave it to the littluns.")

        if tribe == 4 and r.randint(1, 100) < 50 or tribe == 5:
            hunt()


    # Random events
    random_events()
