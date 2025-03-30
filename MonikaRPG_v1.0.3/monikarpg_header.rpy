default persistent._monikarpg_unlocked = False
default persistent._monikarpg_first_time = True

# Register the submod
init -990 python:
    store.mas_submod_utils.Submod(
        author="Icey_Pizza",
        name="Monika RPG",
        description=(
            "Adiciona um novo minigame de RPG! (1.0.3 - Correção de bugs)\n"
            "Está com alguma dúvida? Clique "
            "{a=https://discord.gg/MASBrasil}{b}{i}aqui{/i}{/b}{/a}."
        ),
        version="1.0.3"
    )



init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="MonikaRPG",
            user_name="MASBrasil",
            repository_name="MonikaRPG-PTBR"
        )
