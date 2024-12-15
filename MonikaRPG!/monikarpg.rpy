#TO DO LIST
#Make tutorial
#Chibika minion?
#Monika's special skills

python early:
    import random

# Register the submod
init -990 python:
    store.mas_submod_utils.Submod(
        author="Icey_Pizza",
        name="Monika RPG!",
        description="Adds a new RPG minigame to the play tab! ",
        version="1.0.0"
    )

# Register the submod updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Monika RPG!",
            user_name="IceyPlazza",
            repository_name="MonikaRPG",
            extraction_depth=1
        )

# Unlocking the game conditions
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="rpg_game_unlock",
            conditional="store.mas_games._total_games_played() > 19",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

# initialize game
init 5 python:
    addEvent(
        Event(
            persistent._mas_game_database,
            eventlabel="rpg_start",
            prompt="Monika RPG!",
        ),
        code="GME",
        restartBlacklist=True
    )

# Expand more interesting dialogue
label rpg_game_unlock:
    $ persistent._rpg_unlocked = True
    m 2eub "Hey [player]..."
    m 3rua "I tried unlocking the RPG game for you! Let's see if it works!"
    $ mas_unlockGame("Monika RPG!")
    return

# Start the RPG
label rpg_start:
 
    m 1gua "So you want to fight me eh?"
    m 2dsa "Okay..."
    m 1efa "I accept your challenge!"
    m 3efa "But I must warn you..."
    m 3efa "Those who go against me get deleted."
    m 1hua "Hehe~"
    m 4wsd"But first, would you like a tutorial?"
    menu:
        "Yes":
            jump rpg_tutorial
        "No":
            jump rpg_setup

# Tutorial
label rpg_tutorial:

    "Still under development!"
    jump rpg_setup

# Setup for battle!
label rpg_setup:

    m 1dua "Well..."
    m 1efa "Let the battle begin!"
    "Choose your difficulty."
    menu:
        "Easy":
            $ mhpmax = 1000
            $ m_diff = 0.90
        "Normal":
            $ mhpmax = 1250
            $ m_diff = 1
        "Hard":
            $ mhpmax = 1500
            $ m_diff = 1.125
        "Impossible":
            $ mhpmax = 2000
            $ m_diff = 1.25
    $ mhp = mhpmax
    $ php = 100
    $ potions = 10
    $ protect = 1
    $ protect_turn = 0
    $ mana = 0
    $ atk_buff = 0
    $ phase2 = 0
    $ burn_turn = 0
    $ burn = 0
    $ freeze_turn = 0
    $ swift_turn = 0
    $ swift = 0
    $ heal_turn = 0
    $ m_hitrate = 95
    "Monika has [mhp] HP. You have [php] HP."
    "Your turn."
    jump rpg_menu

# main menu for actions you can take
label rpg_menu:

    $ mana = mana + random.randrange(3,9)
    if php <= 30:
        "You're at critical health!"
        $ mana = mana + random.randrange(2,6)
    elif php <= 50:
        "You are stressed."
        $ mana = mana + random.randrange(1,4)
    if mana >= 100:
        $ mana = 100
        "Your mana is full!"
    menu:
        "Attack (Monika's HP: [mhp])":
            $ attack = random.randrange(15,51) + atk_buff
            #$ attack = 800 # FOR DEBUGGING PURPOSES
            m 1wud "{nw}"
            "You dealt [attack] damage."
            $ mhp = mhp - attack
            if mhp < 0:
                $ mhp = 0
            "Monika now has [mhp] HP left."
            $ atk_buff = 0
            jump rpg_monika

        "Parry (Evasion Bonus: [swift])":
            $ parry = random.randrange(0,100) - swift
            if parry <= 35:
                m 6wud "{nw}"
                "You successfully parried!"
                $ attack = random.randrange(35,71) + atk_buff
                $ atk_buff = 0
                m 6cuo "{nw}"
                "Monika took [attack] reflection damage!"
                $ mhp = mhp - attack
                m 1efa "{nw}"
                if swift_turn > 0:
                    $ swift = random.randrange(10,26)
                jump rpg_menu
            else:
                "You failed to parry."
                jump rpg_monika
            
        "Health Potion ([potions] potions left)":
            if potions > 0:
                jump rpg_heal_sequence
            else:
                "You are out of health potions."
                jump rpg_menu
            
        "Spell (Current mana: [mana])":
            jump choose_spell

        "Surrender (Your HP: [php])":
            stop music fadeout 2.5
            m 1ekd "You're surrendering, [player]?"
            if mhp == mhpmax:
                m 2dkp "But we just started!"
                m 6esc "Maybe we should play again when you have more time..."
            else:
                m 1ekc "Don't be too discouraged."
                m 3eka "You must keep practicing if you want beat me!"
                m 1gka "Well... Maybe next time."
                $ mas_gainAffection(0.25,m_diff+0.1,False)
            $ play_song(persistent.current_track)
            return

# menu for choosing spells
label choose_spell:

    menu:
        "Greater Heal (Lingering Heals) -Cost: 25 mana-":
            if mana >= 25:
                $ heal_amt = random.randrange(60,80)
                $ php = php + heal_amt
                if php > 100:
                    $ php = 100
                $ mana = mana - 25
                "You rejuvinate yourself. You healed [heal_amt] hp!"
                $ heal_turn = 4
                jump rpg_monika
            else:
                "You don't have enough mana."
                jump rpg_menu

        "Fire Sword (Attack Bonus) -Cost: 25 mana-":
            if mana >= 25:
                "You ignite your sword. Your next attack will inflict more damage."
                $ atk_buff = random.randrange(60,121)
                $ mana = mana - 25
                jump rpg_monika
            else:
                "You don't have enough mana."
                jump rpg_menu

        "Freeze (Chance to Immobilize) -Cost: 20 mana-":
            if mana >= 20:
                "You cast a cold wind on Monika."
                if random.randrange(1,101) > 15:
                    m 6wud "{nw}"
                    "Monika is frozen!"
                    $ freeze_turn = 3
                else: 
                    "Monika endured. Freeze failed!"
                $ mana = mana - 20
                jump rpg_monika
            else:
                "You don't have enough mana."
                jump rpg_menu

        "Swift (Evasion Bonus) -Cost: 15 mana-":
            if mana >= 15:
                "You cast a buff on yourself. Your evasion increased!"
                $ swift_turn = 4
                $ mana = mana - 15
                jump rpg_monika
            else:
                "You don't have enough mana."
                jump rpg_menu

        "Fireball (Chance to Burn) -Cost: 15 mana-":
            if mana >= 15:
                $ fb_dmg = random.randrange(35,66)
                $ burn_chance = random.randrange(1,101)
                "You unleash a great fireball. You deal [fb_dmg] damage."
                $ mana = mana - 15
                if burn_chance <= 25:
                    "Monika is set ablaze!"
                    $ burn_turn = 5
                jump rpg_monika
            else:
                "You don't have enough mana."
                jump rpg_menu

        "Protect (Reduce Damage Received) -Cost: 15 mana-":
            if mana >= 15:
                $ protect_turn = 4
                "You shielded yourself. You will take less damage for the next [protect_turn] turns."
                $ mana = mana - 15
                jump rpg_monika
            else:
                "You don't have enough mana."
                jump rpg_menu
            
        "??? (???) -Cost: ???-":
            jump rpg_boop_sequence

        "Cancel Cast? (Current Mana: [mana])":
            jump rpg_menu

# You can choose to heal yourself... or Monika!
label rpg_heal_sequence:
    menu:
        "Use on yourself":
            $ heal_amt = random.randrange(40,56)
            $ php = php + heal_amt
            "You healed [heal_amt] hp!"
            if php > 100:
                $ php = 100
            $ potions = potions - 1
            jump rpg_monika

        "Use on Monika":
            $ heal_amt = random.randrange(50,101)
            $ mhp = mhp + heal_amt
            if mhp > mhpmax:
                $ mhp = mhpmax
            $ potions = potions - 1
            "Monika healed [heal_amt] hp!"
            m 6tko "Wait... you used a health potion on me?"
            m 5tubla "How sweet of you~"
            m 4efu "But this doesn't help your chances of winning!"
            $ mas_gainAffection(0.0125,m_diff+0.1,False)
            jump rpg_monika

# Boop? Boop!
label rpg_boop_sequence:
    menu:
        "What's this?":
            menu:
                "Boop!":
                    m 1wubfd "Huh?!"
                    stop music fadeout 2.5
                    "Monika takes 999999999999 damage."
                    $ play_song(persistent.current_track)
                    m 1hublb "Hahaha~"
                    m 4tublu "I think you found my weakness."
                    m 5fubfa "I love you~"
                    $ mas_gainAffection(0.15,1,False)
                    return "love"

                "Cancel Cast? (Current Mana: [mana])":
                    jump rpg_menu

        "Cancel Cast? (Current Mana: [mana])":
            jump rpg_menu

# Monika's turn! And logic for status effects that should happen during her turn.
label rpg_monika:
    "Monika's turn."
    if protect_turn > 0:
        "You are shielding yourself. Your shield will wear off in [protect_turn] turn(s)."
        $ protect = (float)(random.randrange(1,4))/8.0
        $ protect_turn = protect_turn - 1
    else:
        $ protect = 1
    if heal_turn > 0:
        $ heal_amt = random.randrange(10,16)
        "You feel traces of healing. You heal [heal_amt] hp. The lingering traces will end in [heal_turn] turn(s)."
        $ php = php + heal_amt
        if php > 100:
            $ php = 100
        $ heal_turn = heal_turn - 1
    if swift_turn > 0:
        "You feel fast. Your swiftness will end in [swift_turn] turn(s)."
        $ swift = random.randrange(10,26)
        $ swift_turn = swift_turn - 1
    else:
        $ swift = 0
    if burn_turn > 0:
        $ burn = random.randrange(5,13)
        m 6wud "{nw}"
        "Monika is burning! (-[burn] hp) Monika will stop burning in [burn_turn] turn(s)."
        $ burn_turn = burn_turn-1
        $ mhp = mhp-burn
    if mhp <= mhpmax*0.4 and phase2 == 0:
        jump rpg_monika_phase2
    if mhp <= 0:
        jump rpg_win
    
    if freeze_turn > 0:
        m 6wud "{nw}"
        "Monika is frozen! She will unfreeze in [freeze_turn] turn(s)."
        $ freeze_turn = freeze_turn - 1
        "Your turn."
        jump rpg_menu
    else: 
        $ rng = renpy.random.randint (1, 4)
        if rng == 1:
            m 1efb "It's my turn [player]."
        if rng == 2:
            m 1efb "Try to dodge this!"
        if rng == 3:
            m 1efb "Get ready [player]."
        else: 
            m 1efa "{nw}"
        jump rpg_monika_attack
    return

# Monika does a basic attack (Will add more skills later)
label rpg_monika_attack:
    m 1efa "{nw}"
    $ ran_miss = random.randrange(0,100)
    if (m_hitrate - swift) > ran_miss:
        $ mattack = (int)(round((random.randrange(15,30) + phase2) * protect * m_diff))
        "Monika deals [mattack] damage."
        $ php = php - mattack
    else:
        "Monika missed!"
    if php <= 0:
        jump rpg_lose
    else:
        "Your turn."
        jump rpg_menu
    return

# Monika is now scary...
label rpg_monika_phase2:
    stop music fadeout 2.5
    m 1dusdld "*deep breath*"
    m 1eusdld "Well..."
    m 1eusdlc "I think I underestimated you [player]."
    m 1wfa "But we are not finished."
    call mas_change_weather (mas_weather_thunder, by_user=False)
    m 1wfb "HOW MY BLOOD BOILS!"
    m 1wfb "FACE ME{w=1}, [player]!"
    $ phase2 = 10
    if burn_turn > 0 or freeze_turn > 0:
        $ freeze_turn = 0
        $ burn_turn = 0
        "Monika cleared all status effects!"
    "Monika will permanently inflict more damage."
    "Your turn."
    $ play_song("<loop 0.01>/mod_assets/bgm/eurobeatreality.ogg")
    jump rpg_menu
    return

# Aww, you lost.
label rpg_lose:
    stop music fadeout 2.5
    m 1tua "{nw}"
    "You are dead."
    m 1tub "Well [player]..."
    m 4tuu "I won..."
    m 7hua "But maybe you will have better luck next time."
    m 5hubla "Hehehe~"
    $ play_song(persistent.current_track)
    $ mas_gainAffection(0.4,m_diff+0.1,False)
    return

# Congrats! You won!
label rpg_win:
    stop music fadeout 2.5
    m 6dusdld "Huh..."
    m 6fksdld "[player]..."
    m 6fksdlc "I think I'm too hurt..."
    m 6dksdlc "I..."
    m 6dksdlc "I can't..."
    m 6rkblsdla "..."
    m 1hublb "Hahaha~"
    $ play_song(persistent.current_track)
    m 1tkbla "Just kidding, [mas_get_player_nickname()]."
    m 1ekbla "I'm fine, don't worry."
    m 2tsbla "I didn't think you could beat me."
    m 5ekbfa "That was so much fun, [mas_get_player_nickname()]."
    m 5skbfb "Maybe we should fight again sometime."
    $ mas_gainAffection(1.0,m_diff+0.1,False)
    return