import json
M={}
M['Egg Cream Pop Rock Wafer Sandwiches']=dict(method="""prep: Heat oven to 325°F; line sheets with parchment
creamed = cream until fluffy, 2 min <- Butter + Granulated Sugar
wet = beat in until smooth <- creamed + Whole Milk + Vanilla Extract
dry = whisk <- Flour + Dutch-Process Cocoa Powder + Baking Soda + Salt @wafer
dough = mix on low just until a dough forms <- wet + dry
sheets = roll 1/16 in. between parchment; chill 30 min <- dough
wafers = cut 2 in. rounds (48), re-roll scraps; bake 325°F ~14 min until dry and fully crisp; cool completely <- sheets
base = beat until light and fluffy, 3 min <- Vegetable Shortening + Powdered Sugar + Nonfat Milk Powder + Vanilla Bean Paste + Salt @creme
creme = fold in at the last minute <- base + Popping Candy (unflavored)
pipe ~13 g creme on 24 wafers, top with the rest, press gently; store airtight, 1–2 days before packing <- wafers + creme""",
notes="Wafers crisp further as they cool; if any center flexes once cool, return to the oven 2–3 min. The creme is water-free on purpose so the popping candy keeps its pop — keep the filled sandwiches airtight and assemble close to packing.")

M['Black & White Malted Brownie Cookies']=dict(method="""prep: Heat oven to 350°F; line sheets with parchment
choc = melt together; cool slightly <- Chocolate, Bittersweet + Butter @dark
ribbonD = whip on high to a pale ribbon, 5 min <- Eggs @dark + Dark Brown Sugar @dark + Granulated Sugar @dark + Vanilla Bean Paste @dark
batterD = fold in <- ribbonD + choc
dryD = whisk <- Flour @dark + Dutch-Process Cocoa Powder + Malted Milk Powder @dark + Espresso Powder + Baking Powder @dark + Salt @dark
darkDough = fold just until no streaks; chill 20 min <- batterD + dryD
melted = melt; cool slightly <- Butter @vanilla
ribbonV = whip on high to a pale ribbon, 5 min <- Eggs @vanilla + Dark Brown Sugar @vanilla + Granulated Sugar @vanilla + Vanilla Bean Paste @vanilla
batterV = fold in <- ribbonV + melted
dryV = whisk <- Flour @vanilla + Malted Milk Powder @vanilla + Baking Powder @vanilla + Salt @vanilla
vanillaDough = fold just until no streaks; chill 20 min <- batterV + dryV
scoop ~1 Tbsp of each dough into one ball (24); bake 350°F 12–13 min until edges set; cool 5 min on sheet <- darkDough + vanillaDough""",
notes="Centers look underdone at 12 min and set as they cool. Test one sheet first: the vanilla half has no cocoa butter, so it may spread a little more — chill longer if it does.")

M['Cherry Phosphate Shortbread Thumbprints']=dict(method="""prep: Day before: start the wild cherry syrup (see notes; make one batch for the whole plan)
prep: Heat oven to 350°F; line sheets with parchment
extract = macerate 24 h; strain; re-steep bark in warm water 1 h; strain; combine <- Wild Cherry Bark + Vegetable Glycerin + Water
juiced = add; top up with water to volume <- extract + Tart Cherry Juice
syrup = dissolve without heat (use 2 Tbsp per batch) <- juiced + Granulated Sugar @syrup
jam = simmer back to a thick jam; cool completely <- Sour Cherry Preserves + syrup
filling = stir in off heat, to taste <- jam + Acid Phosphate Solution
creamed = cream until fluffy, 2 min <- Butter + Granulated Sugar @dough + Honey
wet = beat in <- creamed + Egg Yolks + Cherry Extract + Almond Extract
dry = whisk <- Flour + Freeze-Dried Cherry Powder + Baking Powder + Salt
dough = mix on low just until combined <- wet + dry
shaped = roll 1 in. balls (~19 g), press wells; chill on sheets while oven heats <- dough
baked = fill ~½ tsp each; bake 350°F 12–13 min until edges just set; cool on sheet 5 min <- shaped + filling
dust when cool <- baked + Powdered Sugar""",
notes="WILD CHERRY SYRUP (Art of Drink, https://www.artofdrink.com/soda/cherry-phosphate) — full recipe makes 12 fl oz: 1 oz wild cherry bark, 1 fl oz glycerin, 4 fl oz water (first maceration), 4 fl oz warm water (second), 4 fl oz cherry juice, 10 oz sugar. One-third of the recipe covers 4 batches. ACID PHOSPHATE: the ⅔ tsp per batch keeps the drink's ratio (1 tsp per 1½ oz syrup) for traditional acid phosphate; with MacSweetie's, add drops to the cooled jam to taste and record the count. Built on your Jam Thumbprint proportions (yolk only, no added liquid, no baking soda) so the wells hold.")

M['Coca-Cola Molasses Crinkle Cookies']=dict(method="""prep: Reduce Coca-Cola to molasses strength — 141 g syrup per liter of Coke; cool (see notes)
prep: Heat oven to 350°F; line sheets with parchment
base = whisk until smooth <- Vegetable Oil + Granulated Sugar @dough + Dark Brown Sugar
wet = whisk in <- base + Reduced Coca-Cola Syrup + Eggs + Vanilla Extract
dry = whisk <- Flour + Ground Ginger + Ground Cinnamon + Ground Cloves + Baking Soda
dough = fold just until no flour streaks <- wet + dry
balls = roll 1½ in. balls (~30 g); roll generously in sugar <- dough + Granulated Sugar @coating
bake 350°F 8–10 min until cracked with soft centers; cool 5 min on sheet <- balls""",
notes="COLA SYRUP: Mexican Coke has ~110 g sugar per liter; reducing each liter to ~141 g (≈100 ml) matches molasses' ~22% water. Weigh the empty pot, simmer flat Coke in stainless or enameled (not aluminum/cast iron), and reduce until it weighs 141 g per liter started (2 L → ~282 g); it will bubble around 225°F near the end but trust the scale. Optional: a little lime zest or cola extract stirred into the cooled syrup for more cola aroma. If a test cookie tastes faintly soapy/metallic, cut baking soda to 8 g.")

M["Root Beer Float Millionaire's Bars"]=dict(method="""prep: Heat oven to 350°F; line a 9×13 pan with a parchment sling
creamed = cream until light, 3 min <- Butter @crust + Granulated Sugar @crust + Dark Brown Sugar @crust
wet = beat in <- creamed + Egg Yolks + Vanilla Bean Paste @crust
crumbs = mix on low until crumbly <- wet + Flour + Salt @crust
crust = press evenly into pan; bake 350°F 25 min until edges are golden; cool <- crumbs
cooked = cook over medium-low, stirring constantly, to 240°F (soft ball) <- Dark Brown Sugar @caramel + Granulated Sugar @caramel + Butter @caramel + Sweetened Condensed Milk + Corn Syrup + Heavy Cream
caramel = off heat, stir in <- cooked + Vanilla Extract + Sarsaparilla / Root Beer Extract + Ground Star Anise
layered = pour over crust; set until firm, ~2 h <- crust + caramel
melted = melt gently <- Chocolate, White + Vanilla Bean Paste @top
spread ~2 mm thin over the caramel; sprinkle salt; set; cut 24 bars with a hot knife <- layered + melted + Flaky Sea Salt""",
notes="Keep the white-chocolate layer thin so it reads as vanilla ice cream rather than candy. Caramel method after Clever Pink Pirate's root beer caramel (https://cleverpinkpirate.com/root-beer-caramel-recipe/). Bars are large (~75 g); cut 48 for cookie-box size.")

M['Lime Rickey Drops']=dict(method="""prep: Heat oven to 350°F; line sheets with parchment
zested = rub together until fragrant <- Granulated Sugar + Lime Zest @dough
creamed = cream until fluffy, 2 min <- zested + Butter
wet = beat in; it may look curdled <- creamed + Eggs + Sour Cream + Lime Juice @dough + Vanilla Extract
dry = whisk <- Flour + Baking Powder + Baking Soda + Salt
dough = mix on low just until combined; chill 30 min <- wet + dry
cookies = scoop 2 Tbsp (~30 g); bake 350°F 9–11 min, just set and not browned; cool completely <- dough
glaze = whisk smooth <- Powdered Sugar + Lime Juice @glaze + Citric Acid
dip tops; finish with zest; set 30 min <- cookies + glaze + Lime Zest @glaze""",
notes="Pull them while pale so they stay soft and cakey. The citric acid goes in the glaze (not sprinkled on top) so it doesn't weep in the mail. Optional: a tiny drop of green gel in the glaze.")

patch={'id':'2026-11-methods','methods':[{'recipe':k,'method':v['method'],'notes':v['notes'],'overwrite':True} for k,v in M.items()]}
json.dump(patch,open('/home/claude/work/patch-2026-11-methods.json','w'),indent=1)
print('ok')
