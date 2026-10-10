"""Illustrative regional priors (Pune area). Replace with eBird frequency data for real use."""
RARITY={"common":0.9,"uncommon":0.5,"rare":0.15,"vagrant":0.02}
ALL=range(1,13);DAY=(5,19);NIGHT=(18,6)
# name: (rarity, months, active-hours window)
S={"Oriental Magpie-Robin":("common",ALL,DAY),"Indian Robin":("common",ALL,DAY),"Common Tailorbird":("common",ALL,DAY),
"Coppersmith Barbet":("common",ALL,(5,18)),"Asian Koel":("common",range(3,9),(4,11)),"Red-vented Bulbul":("common",ALL,DAY),
"Purple Sunbird":("common",ALL,DAY),"Common Myna":("common",ALL,DAY),"Rose-ringed Parakeet":("common",ALL,DAY),
"White-throated Kingfisher":("common",ALL,DAY),"Spotted Owlet":("uncommon",ALL,NIGHT),"Indian Pitta":("rare",range(5,10),(5,9)),
"Brown Hawk-Owl":("rare",ALL,NIGHT)}
def in_window(h,w):a,b=w;return a<=h<=b if a<=b else h>=a or h<=b
def prior(name,month,hour):
    if name not in S:return RARITY["vagrant"]
    r,months,w=S[name];p=RARITY[r]
    if month not in months:p*=0.2
    if not in_window(hour,w):p*=0.3
    return round(p,3)
