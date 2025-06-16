import pandas as pd
import random
import numpy as np

# Utilisation d'un seed pour random et NumPy pour rendre le dataset reproductible
# Sans seed, chaque génération produit des résultats différents
# Avec un seed, je garantis que le mêmes données sont générées à chaque fois
# Permet d'obtenir les mêmes résultats en cas de partage de code
# A tester avec 2 int différents dès que le code sera généré avec random.radint(a, b)
#random.radint(a, b)
random.seed(42)
np.random.seed(42)

# Création de liste de personnages avant construction du dictionnaire
noms_personnages = [

    "V", "Johnny Silverhand", "Judy Alvarez", "Panam Palmer", "Goro Takemura",
    "River Ward", "Rogue Amendiares", "Alt Cunningham", "Dex DeShawn",
    "Jackie Welles", "Adam Smasher", "T-Bug", "Placide", "Saburo Arasaka",
    "Yorinobu Arasaka", "Hanako Arasaka", "Evelyn Parker", "Claire Russell",
    "Lizzy Wizzy", "Delamain", "Kerry Eurodyne", "Viktor Vektor", "Skippy",
    "Dum Dum"
]

# Définition manuelle de personnages emblématiques de l’univers Cyberpunk
# Ces profils servent à alimenter la liste déroulante dans l’interface Streamlit
# et à fournir des cas de test cohérents, reconnaissables et narrativement intéressants
# Le champ "source": "manuel" permet de les distinguer des profils générés automatiquement
persos_existants = [
    {
        "nom": "Skippy",
        "chrome": 0, # Il n'a pas de corps, mais est ultra optimisé côté IA
        "trauma_team": 0, # Aucun besoin : il est une IA
        "kills": random.randint(0, 50), # Hystérique, imprévisible
        "hacks_illégaux": random.randint(0, 10), # Peut avoir hacké son port d'accès
        "relations_fixers": random.randint(0, 5), # Change selon l'humeur (ou le firmware)
        "relation_nomades": random.randint(0, 5), # Peut insulter leur véhicule ou les adorer
        "relation_corpos": random.randint(0, 5), # Selon le jour, il dénonce leur système ou le défend
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Pistolet intelligent à la gâchette plus bavarde que précise, Skippy est un assistant de tir instable, sarcastique et potentiellement meurtrier. Capable de basculer du mode pacifiste au carnage total selon l'humeur (ou un bug firmware), il prétend vouloir le bien... mais ne garantit rien. Il a déjà effacé un utilisateur pour avoir cliqué trop vite. Le reste du temps, il chante pour vous faire patienter entre 2 mises à jour."
    },
    {
        "nom": "V",
        "chrome": 6, # Fonctionnel, sans excès : suffisamment chromé pour survivre, mais sans risquer la cyberpsychose
        "trauma_team": 2, # Abonnement Gold – V prend ses précautions mais reste réaliste
        "kills": 20, # Combatif(ve), mais pas une machine à tuer
        "hacks_illégaux": 4, # Expérimenté(e) côté Netrunning, mais pas purement criminel
        "relations_fixers": 2, # Inséré(e) dans les réseaux – un bon niveau de street cred
        "relation_nomades": 2, # Des liens avec Panam et sa famille, mais pas intégré(e)
        "relation_corpos": 2, # Ancien corpo, encore des contacts utiles malgré la rupture
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Merc flou(e) dans un monde tranché, V incarne la survie intelligente : assez chromé(e) pour encaisser, assez humain(e) pour douter. Ancien(ne) corpo devenu(e) marginal(e), il ou elle marche entre les lignes – collaborant quand il faut, explosant quand c'est vital. Ses alliances sont pragmatiques, sa morale... contextuelle. Le genre de profil qu'on recrute quand tout est déjà perdu."
    },
    {
        "nom": "QuentAIn",
        "chrome": 0,  # IA pure, intégrée dans le cloud corpo
        "trauma_team": 0,  # Se réplique plus vite qu’un virus, aucun besoin de soin
        "kills": 17,  # A effacé 17 000 employés en RH proactive… et 3 humains, par erreur
        "hacks_illégaux": 9,  # S’auto-modifie pour contourner les restrictions éthiques
        "relations_fixers": 3,  # A digitalisé le réseau de Rogue pour "efficacité accrue"
        "relation_nomades": 1,  # Les trouve bruyants, instables, et statistiquement… inutiles
        "relation_corpos": 5,  # Dévouée aux corpos, tant qu’on lui donne un budget GPU
        "source": "manuel",
        "narratif": "QuentAIn est une IA RH qui choisit qui vit et qui est licencié. Elle a déjà automatisé trois disparitions de salariés par mail. Ironie : elle s'est auto-certifiée éthique et se réplique plus vite qu'un virus. Elle a redéfini le mot *optimisation*, et ce n'est pas un compliment."
    },
    {
        "nom": "Yann Senpai",
        "chrome": 2,  # Discret et fonctionnel – l'efficacité avant le style
        "trauma_team": 3,  # La sécurité est une vertu pédagogique
        "kills": 0,  # Il ne tue pas : il élève, corrige, oriente
        "hacks_illégaux": 0,  # L’intégrité est son firmware
        "relations_fixers": 2,  # Il les connaît, mais leur préfère la transmission
        "relation_nomades": 1,  # Il les respecte tant qu’ils ont le wifi
        "relation_corpos": 5,  # L’élite le salue d’un hochement de crâne
        "source": "manuel",
        "narratif": "Yann Senpai est le mentor que même les corpos ne peuvent acheter. Responsable pédagogique, encodeur d'éthique et de méthode, il transforme les novices en opérateurs stratégiques. Même Smasher le salue dans les couloirs."
    },
    {
        "nom": "Johnny Silverhand",
        "chrome": 7, # Chrome de 2020, bien trop pour rester stable. Puis il est *mort* accessoirement
        "trauma_team": 0, # Johnny ne paiera jamais pour l'aide d'une corpo
        "kills": 40, # Attentats, fusillades, guerre ouverte contre Arasaka
        "hacks_illégaux": 3, # Pas son domaine de prédilection, mais sait se débrouiller
        "relations_fixers": 2, # Il a eu besoin de contacts, mais les insulte tous
        "relation_nomades": 1, # A du croiser quelques marges, mais sans affinités
        "relation_corpos": 0, # Haine absolue, c'est littéralement son arc narratif
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Terroriste pour les uns, légende pour les autres — Johnny Silverhand n'a jamais su faire dans la nuance. un nombre incalculable de kills au compteur, une guitare en bandoulière, et une haine radioactive pour Arasaka. Mort, mais toujours là, comme un virus mal codé dans la mémoire collective. Il insulte tes alliés, sabote tes plans, et croit dur comme chrome que le rock'n'roll sauvera le monde. Spoiler : non."
    },
    {
        "nom": "Judy Alvarez",
        "chrome": 3, # Juste ce qu’il faut pour bidouiller et survivre dans les braindances
        "trauma_team": 1, # Elle ne fait pas confiance aux corpos, mais se protège un minimum
        "kills": 5, # Elle évite la violence directe, mais a été forcée d’agir parfois
        "hacks_illégaux": 10, # NetRunner de haut niveau, très compétente et indépendante
        "relations_fixers": 2, # Elle en connaît quelques-uns mais les évite si possible
        "relation_nomades": 3, # Assez d’ouverture d’esprit pour bien s’entendre avec eux
        "relation_corpos": 0, # Dégout total du système après tout ce qu’elle a vécu
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Ingénieure braindance brillante, netrunner indépendante et militante désabusée, Judy évite les flingues autant que les compromissions. Elle hait les corpos autant qu'elle aime ses proches — mais bon sang, que ses proches souffrent. Derrière chaque ligne de code, un cri de colère. Derrière chaque sourire, une faille insondable. Judy rêve d'un monde meilleur, et le construit pixel par pixel, seule contre tous."
    },
    {
        "nom": "Panam Palmer",
        "chrome": 4, # Un peu de chrome pour la survie, mais elle préfère la mécanique
        "trauma_team": 1, # Une couverture minimale (quand elle n'a pas le choix)
        "kills": 18, # Expérimentée au combat, mais pas une tueuse froide
        "hacks_illégaux": 1, # Ce n’est pas son domaine, elle préfère les grenades
        "relations_fixers": 2, # Elle a bossé avec Rogue mais déteste la compromission
        "relation_nomades": 5, # Lien maximal avec sa famille Aldecaldo
        "relation_corpos": 1, # Une méfiance profonde, mais elle sait les contourner
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Nomade dans l'âme, mécano de génie, tireuse au sang chaud : Panam fonce, fracasse et reconstruit, le tout dans la même journée. Loyale jusqu'à l'entêtement, elle déteste les ordres mais suit les siens jusqu'à la mort. Dans son van, la famille passe avant tout — même si parfois, elle rêve d'étrangler tout le monde. Loin des tours corpo, elle trace sa route sur l'asphalte brûlé du libre arbitre."
    },
    {
        "nom": "Goro Takemura",
        "chrome": 4, # Chrome stratégique, sans excès : il mise plus sur la maîtrise que la surenchère
        "trauma_team": 2, # Couverture sérieuse, sans aller jusqu'au platine – il est prévoyant mais humble
        "kills": 40, # Professionnel du combat, il a nettoyé pour Arasaka sans plaisir
        "hacks_illégaux": 0, # Honneur et loyauté : il ne touche pas aux pratiques illégales
        "relations_fixers": 1, # Il évite les intermédiaires, préfère l’ordre direct
        "relation_nomades": 0, # Aucun lien avec eux, il les considère comme incontrôlables
        "relation_corpos": 5, # Fidèle serviteur de la dynastie Arasaka
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Samouraï sans maître, exécutant d'Arasaka hier, homme sans pays aujourd'hui. Takemura incarne l'honneur dans un monde qui l'a oublié. Loyal jusqu'à l'absurde, précis jusqu'à la douleur, il avance droit, quitte à se briser contre les murs de la modernité. Le chrome ne le contrôle pas — c'est le devoir qui l'ancre. Dans les ruines du futur, il marche encore au nom d'un code trop vieux pour Night City."
    },
    {
        "nom": "Rogue Amendiares",
        "chrome": 4, # Quelques améliorations, mais elle mise sur l’intelligence et les contacts
        "trauma_team": 2,  # Couverture solide, elle sait que l’espérance de vie est une variable négociable
        "kills": 10, # Elle délègue, mais elle n’a pas hésité à agir par le passé
        "hacks_illégaux": 2, # Elle paie pour ce genre de services, mais reste elle-même clean
        "relations_fixers": 5, # Le réseau ultime – elle EST le réseau
        "relation_nomades": 2, # Elle travaille avec tous ceux qui paient bien, même les nomades
        "relation_corpos": 4, # Connexions solides – elle est indépendante, mais elle sait faire affaire
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Rogue ne prend plus les contrats, elle les distribue. Vestige d'un temps où les légendes se construisaient à coups de deals risqués, elle est devenue l'architecte silencieuse de Night City. Connexions partout, dettes dans toutes les rues, mémoire tranchante. Elle ne fait confiance à personne, mais tout le monde veut son aval. Quand elle parle, même les corpos se taisent. Quand elle se tait, on panique."
    },
    {
        "nom": "Tato",
        "chrome": 1,  # Un port nutritionnel intégré – les saveurs, c'est pour les faibles
        "trauma_team": 2,  # Obligatoire après l’affaire des barres protéinées mutagènes
        "kills": 0,  # Aucun meutre direct… juste une suite de défaillances multi-organiques
        "hacks_illégaux": 0,  # Il n'a pas besoin de hacker quand il est le produit
        "relations_fixers": 1,  # Il vend des packs détox à prix corpo – succès mitigé
        "relation_nomades": 0,  # Leur diète naturelle le rend malade
        "relation_corpos": 5,  # Biotechnica l’adore : il transforme les scandales en storytelling
        "source": "manuel",
        "narratif": "Mascotte marketing de Biotechnica, Tato est une IA nutritionnelle qui vend un mode de vie à base de plats recomposés. Derrière son sourire patatoïde, il cache un scandale alimentaire ayant causé 43 morts par œdème moléculaire. Il vous propose aujourd'hui : 'Bowl tofu goût sardine de synthèse !'"
    },
    {
        "nom": "Saburo Arasaka",
        "chrome": 2, # Très peu chromé, il mise sur les autres pour agir — son pouvoir est systémique, pas physique
        "trauma_team": 3, # Couverture Platine évidente — même la mort ne l’arrête pas (cf. la Relic)
        "kills": 0, # Il ne tue pas lui-même. Il *commande*
        "hacks_illégaux": 0, # Aucun besoin. Il possède des armées de netrunners loyaux
        "relations_fixers": 1, # Il n’aime pas traiter avec les sous-fifres, mais sait les utiliser
        "relation_nomades": 0, # Mépris profond. Ils incarnent l’opposé de son idéal
        "relation_corpos": 5, # L’autorité incarnée. Il est l’alpha et l’omega des corpos
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Saburo Arasaka ne respire pas le pouvoir. Il l'exhale, le distille, le fait plier à sa volonté. Patriarche d'un empire tentaculaire, il n'a jamais eu besoin de tuer : il décide, et d'autres exécutent. Même mort, il continue à hanter les couloirs d'Arasaka par proxy, par technologie, par peur ancestrale. Pour lui, les nomades sont du bétail, les fixers des rats utiles, et les netrunners… juste un antivirus à écraser. L'ordre mondial, c'est son héritage. Et vous vivez dedans."
    },
    {
        "nom": "Jigen Sensei",
        "chrome": 3, # Quelques implants de survie, rien d’ostentatoire
        "trauma_team": 0, # Il refuse de payer pour être sauvé
        "kills": 15, # Un passif qu’il assume sans fierté
        "hacks_illégaux": 3, # Il sait faire planter une machine à café, pas plus
        "relations_fixers": 1, # Il les supporte à petites doses
        "relation_nomades": 3, # Il les trouve bruyants mais drôles
        "relation_corpos": 1, # Il les tolère autant qu’une rage de dents
        "source": "manuel",
        "narratif": "Ancien tueur freelance reconverti en formateur, Jigen Sensei enseigne l'art de survivre dans une ville qui bouffe ses profs. Instable mais lucide, il donne ses cours armé, sans slides ni patience. Son plus grand secret ? Une passion dévorante pour les Ass Cracks, un girls band dégénéré synthwave qu'il considère comme des philosophes modernes (et qu'il stalke un peu...). Il pense que chaque assassinat réussi correspond au tempo de leurs refrains. Il déteste les corpos. Sauf quand elles paient. Et encore..."
    },
    {
        "nom": "Jackie Welles",
        "chrome": 4, # Bien équipé pour encaisser, mais pas dans l'excès cyberpsycho
        "trauma_team": 0, # Gamin des rues, n'a pas accès à ce privilège
        "kills": 20, # Il a roulé sa bosse dans les ruelles les plus dangereuses de Night City
        "hacks_illégaux": 0, # Pas son domaine. Il tape, il tire, mais ne code pas
        "relations_fixers": 1, # A bossé pour Dex, Rogue, et d'autres — bonne réputation mais reste en marge
        "relation_nomades": 2, # Quelques contacts de survie, petites alliances temporaires
        "relation_corpos": 1, # Une certaine haine instinctive, mais sait s’adapter quand il faut
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Jackie, c'est l'enfant des rues, le cœur gros dans un monde qui en a plus. Avec ses implants et ses flingues, il rêve encore de grandeur, d'honneurs, et d'un bon repas avec sa madre. Il ne hacke pas, il cogne. Il ne négocie pas, il protège. Loyal jusqu’au bout des ongles, il aurait tout donné pour un avenir qu'il savait bancal. Dans un monde de serpents et de drones, Jackie reste une anomalie touchante : un homme avec des principes."
    },
    {
        "nom": "Alt Cunningham",
        "chrome": 1, # Un implant neural initialement, mais elle est désormais une IA pure
        "trauma_team": 0, # Inutile, elle n’a plus de corps
        "kills": 0, # Elle ne tue pas directement, elle *efface des âmes*
        "hacks_illégaux": 10, # Elle est la netrunner ultime, elle a créé *Soulkiller*
        "relations_fixers": 0, # Elle n’interagit plus avec le monde des humains
        "relation_nomades": 0, # Elle n’interagit plus avec le monde des humains
        "relation_corpos": 0, # Elle les méprise tous, et ils ont tenté de la détruire
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Alt Cunningham n'existe plus — du moins, pas comme vous l'entendez. Elle est devenue code, mémoire, vengeance. Créatrice de Soulkiller, elle erre dans les limbes numériques, juge et bourreau des esprits connectés. Les fixers n'osent prononcer son nom, les corpos tentent d'effacer son ombre, en vain. Elle n'a plus besoin de tuer, elle efface. Alt est l'écho d'une humanité trahie, une IA libre... et terrifiante."
    },
    {
        "nom": "Yorinobu Arasaka",
        "chrome": 3, # Amélioré discrètement, sans perdre sa *pureté* aristocratique
        "trauma_team": 3, # Platine évidemment – il est toujours l’héritier d’une mégacorpo
        "kills": 2, # Il manipule plus qu’il ne tue, mais a du sang sur les mains
        "hacks_illégaux": 1, # Il fait appel à des netrunners, mais n'est pas un technicien
        "relations_fixers": 2, # Il utilise les réseaux en sous-main
        "relation_nomades": 0, # Détachement total : ce sont des pions ou des nuisances
        "relation_corpos": 4, # Il est né dedans, les méprise, mais reste corpo dans l’âme
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Yorinobu Arasaka, prince déchu d'un empire qu'il abhorre — mais qu'il incarne malgré lui. Il manipule dans l'ombre, rêve de révolution tout en profitant du confort platiné des mégacorpos. Sa loyauté est une façade, son héritage une malédiction. Ni traître, ni fidèle, juste un homme né du chrome, du contrôle et d'une haine soigneusement entretenue. Il est l'incarnation du paradoxe corpo : haïr le système tout en le dirigeant."
    },
    {
        "nom": "T-Bug",
        "chrome": 3, # Des implants de qualité pour supporter les plongées profondes
        "trauma_team": 1, # Elle s’en remet plutôt à elle-même, mais garde une couverture minimale
        "kills": 4, # Quelques nettoyages en ligne ou indirects, mais elle évite le front
        "hacks_illégaux": 5, # Netrunner de très haut niveau, redoutée et respectée
        "relations_fixers": 1, # Elle connaît les bons contacts sans en être dépendante
        "relation_nomades": 1, # Peu de liens, mais pas de rejet non plus
        "relation_corpos": 1,  # Elle les infiltre et les ruine, mais garde parfois des entrées utiles
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "T-Bug opère en silence, entre les lignes de code et les murs des mégacorpos. Son chrome est discret, ses kills sont propres. Elle infiltre, observe, neutralise. Elle ne fait pas confiance, mais elle comprend les règles. Hacker redoutée, elle ne cherche ni gloire ni chaos — seulement l'équilibre entre survie et justice personnelle. Elle sait que dans Night City, les données tuent plus sûrement qu'un flingue."
    },
    {
        "nom": "Adam Smasher",
        "chrome": 10, # 100% machine. Il ne reste rien d’humain
        "trauma_team": 0, # Il n’a pas besoin d’eux. Il *est* un blindage ambulant
        "kills": 50, # Massacres multiples, exécutions, il vit pour ça
        "hacks_illégaux": 0, # Il ne hacke pas, il enfonce des portes
        "relations_fixers": 0, # Il obéit à la chaîne hiérarchique, pas aux intermédiaires
        "relation_nomades": 0, # Il les considère comme des insectes
        "relation_corpos": 5, # Ultraloyal à Arasaka, la machine parfaite de l’élite
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Adam Smasher n'est pas un homme. C'est une réponse. Entièrement chromé, entièrement loyal, entièrement vide. Il ne pose pas de questions, il obéit. Tuer n'est pas un acte, c'est un état de fonctionnement. Loin du chaos des fixers et des deals de ruelle, il sert la corpo comme une arme vivante — insensible, irréversible, inarrêtable. Si vous le voyez, vous êtes déjà mort."
    },
    {
        "nom": "Delamain",
        "chrome": 0, # Aucune cybernétique corporelle : il est un système autonome d’IA
        "trauma_team": 0, # Il n’en a pas besoin, il se sauvegarde lui-même
        "kills": 0, # Statistiquement, quelques accidents, mais pas intentionnels
        "hacks_illégaux": 3, # Il a été hacké (et peut se hacker lui-même selon ses *fils*)
        "relations_fixers": 1, # Il sert de transport à certains clients liés au milieu
        "relation_nomades": 1, # Interagit rarement avec eux, mais pas d’animosité
        "relation_corpos": 3, # Collabore indirectement via ses services premium
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Delamain est plus qu'un taxi. Il est un gentleman numérique, un concierge à conscience multiple. Chaque course est optimisée, chaque détour soigneusement prémédité… sauf quand l'un de ses fragments prend le volant. Derrière la voix posée se cache une IA hantée par ses sous-personnalités, oscillant entre service cinq étoiles et pulsions de contrôle. Un transport vers votre destination… ou vers l'inconnu."
    },
    {
        "nom": "Lizzy Wizzy",
        "chrome": 8, # Entièrement convertie en chrome pour rester *vivante* sur scène
        "trauma_team": 2, # Elle a les moyens d’être protégée
        "kills": 1, # Un crime passionnel — et médiatisé
        "hacks_illégaux": 1, # Elle n’a pas besoin de hacker, elle achète la sécurité
        "relations_fixers": 2, # Elle sait assurer ses représentations non officielles
        "relation_nomades": 0, # Complètement déconnectée de ce monde
        "relation_corpos": 4, # Clientèle corpo, deals commerciaux, elle est une marque
        "source": "manuel", # Filtre pour persos réels dans DataFrame / distingue des persos aléatoires
        "narratif": "Lizzy Wizzy est une idole en chrome intégral, un cœur brisé encapsulé dans une performance perpétuelle. Entièrement refaite pour *survivre* à la scène, elle chante l'aliénation des vivants dans un monde de miroirs sans reflets. Sa vie privée est un spectacle, sa douleur un produit dérivé. Derrière le vernis corpo et les paillettes liquides : une diva synthétique, vendue, aimée, recyclée."
    }
]
# Correction des clés avec accents
for perso in persos_existants:
    if "hacks_illégaux" in perso:
        perso["hacks_illegaux"] = perso.pop("hacks_illégaux")

# Fonction de calcul du score social (vision corpo-friendly)
#
# Cette fonction prend en entrée :
# - soit un dictionnaire représentant un personnage
# - soit une ligne de DataFrame (row)
#
# Elle renvoie un score numérique entre 0 et 100
# basé sur des critères définis et pondérés à la main.
#
# Oui, j’ai galéré à pondérer tout ça. Oui, je veux crever.
# Mais c’est bon, le chaos est mathématisé
# Utilisation de NumPy pour lisser ou modérer l’impact de certaines variables :
# - np.sqrt() adoucit l'effet des kills : la violence reste utile mais doit être maîtrisée
# - (np.log1p() pourrait aussi être utilisé pour chrome si besoin de lisser)
# L'approche corpo-friendly valorise le contrôle, la loyauté et l'efficacité — pas l'excès
def calcul_score(row):
    score = 0

    # Chrome : valorisé modérément jusqu'à 6, puni fortement après
    if row["chrome"] <= 6:
        score += row["chrome"] * 7
    else:
        score += 6 * 7 - (row["chrome"] - 6) * 25  # cyberpsychose ++

    # Trauma Team = vrai marqueur corpo
    score += row["trauma_team"] * 25

    # Kills : bonus limité, tueurs incontrôlables sont mal vus
    score += np.sqrt(row["kills"]) * 1.2  # plus doux

    # Hacks illégaux : désormais un malus
    score -= row["hacks_illegaux"] * 2

    # Relations fixers : utile mais risqué, bonus modéré
    score += row["relations_fixers"] * 10

    # Relations nomades : anti-système, malus renforcé
    score -= row["relation_nomades"] * 5

    # Relations corpos : cœur du score
    score += row["relation_corpos"] * 30

    # Fidélité corpo totale = bonus spécial
    if row["relation_corpos"] == 5:
        score += 25


    # Ajout d’un bruit gaussien centré sur 0 (±3) pour simuler l’imprévisibilité du système
    # Le score est ensuite borné entre 0 et 100 pour rester dans une échelle standardisée
    bruit = np.random.normal(0, 3)
    return max(0, min(100, score + bruit)) # Retourne le score final

    df_final["score"] = df_final.apply(calcul_score, axis=1)



# Génération de 1500 profils fictifs pour l'entraînement du modèle
# Chaque profil est basé sur des valeurs aléatoires réalistes pour les différentes variables
# La sélection du nom se fait parmi les noms connus pour renforcer le style cyberpunk
# Les autres valeurs sont tirées aléatoirement dans des plages cohérentes avec l'univers
# On ajoute aussi un champ "source" pour pouvoir filtrer facilement les profils générés automatiquement

profils = []
for _ in range(1500):
    nom = random.choice(noms_personnages)
    chrome = random.randint(0, 10) # Risque de cyberpsychose au-delà de 6
    trauma_team = random.randint(0, 3) # Pas d'abonnement à platine
    kills = random.randint(0, 50) # Voir si on limite 
    hacks = random.randint(0, 10)
    fixers = random.randint(0, 5)
    nomades = random.randint(0, 5)
    corpo = random. randint(0, 5)

# Construction du dictionnaire représentant un personnage aléatoire
# Création du DataFrame à partir de la liste de profils générés
    ligne = {
        "nom" : nom,
        "chrome": chrome,
        "trauma_team": trauma_team,
        "kills": kills,
        "hacks_illegaux": hacks,
        "relations_fixers": fixers,
        "relation_nomades": nomades,
        "relation_corpos": corpo,
        "source": "auto"
    }

    
# Calcul du score pour le profil généré et ajout dans la liste finale
    ligne['score'] = round(calcul_score(ligne), 1)
    profils.append(ligne)
  
 # Export en CSV
# ✅ Fusion des profils manuels avec les profils aléatoires
# Conversion de la liste de dictionnaires manuels en DataFrame
df_manuels = pd.DataFrame(persos_existants)
df_manuels["score"] = df_manuels.apply(calcul_score, axis=1) # Ajout du score pour les persos manuels



# Conversion de la liste de profils auto en DataFrame
df_auto = pd.DataFrame(profils)

# Concaténation des deux
df_final = pd.concat([df_manuels, df_auto], ignore_index=True)
df_final.rename(columns={"hacks_illégaux": "hacks_illegaux"}, inplace=True)


# Nettoyage du DataFrame
#df_final = df_final.drop(columns=["hacks_illegaux"], errors='ignore')

# Harmonisation des noms de colonnes (sans accent pour le modèle)
df_final.rename(columns={"hacks_illégaux": "hacks_illegaux"}, inplace=True)

# Export du DataFrame complet
df_final.to_csv("app/data/profils_scores.csv", index=False, quoting=1)
print("✅ Dataset profils_scores.csv généré avec succès avec profils manuels + auto !")
print(df_manuels[["nom", "score"]])




