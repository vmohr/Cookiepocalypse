import json
seed=json.load(open('/home/claude/app/seed.json'))
byname={r['name']:r for r in seed['recipes']}
def I(phase,name,amount,unit,grams=None):
    d={'name':name,'amount':amount,'unit':unit,'phase':phase}
    if grams is not None: d['grams']=grams
    elif unit=='Grams': d['grams']=amount
    return d
src=' (Retro Soda Fountain 2026; base batch = 24.)'

egg={'name':'Egg Cream Pop Rock Wafer Sandwiches','book':'Custom (wafer after King Arthur-style chocolate wafers)','bookUrl':'','page':'N/A',
 'cookiesPerBatch':24,'refrigerate':'Chill rolled dough 30 min','ovenTemp':'325','bakeMinutes':14,
 'notes':'Crisp chocolate wafers sandwiching a milky "egg cream" creme with popping candy. WAFERS: cream butter + sugar, beat in milk + vanilla, mix in dry. Roll 1/16 in. thin between parchment, chill 30 min, cut 2 in. rounds (48 wafers). Bake at 325°F about 14 min until dry and fully crisp; they crisp more as they cool. CREME: beat shortening, powdered sugar, milk powder, vanilla and salt until fluffy. It is water-free on purpose so the popping candy keeps its pop. Fold in popping candy last, pipe about 13 g per sandwich and sandwich gently without squishing. Assemble 1-2 days before packing and store airtight.'+src,
 'ingredients':[
  I('Wafer Dough','Flour',150,'Grams'),I('Wafer Dough','Dutch-Process Cocoa Powder',45,'Grams'),I('Wafer Dough','Baking Soda',1.2,'Grams'),I('Wafer Dough','Salt',2,'Grams'),
  I('Wafer Dough','Butter',115,'Grams'),I('Wafer Dough','Granulated Sugar',170,'Grams'),I('Wafer Dough','Whole Milk',45,'Milliliters'),I('Wafer Dough','Vanilla Extract',5,'Milliliters'),
  I('Egg Cream Creme','Vegetable Shortening',85,'Grams'),I('Egg Cream Creme','Powdered Sugar',200,'Grams'),I('Egg Cream Creme','Nonfat Milk Powder',30,'Grams'),
  I('Egg Cream Creme','Vanilla Bean Paste',5,'Milliliters'),I('Egg Cream Creme','Salt',1,'Grams'),I('Egg Cream Creme','Popping Candy (unflavored)',60,'Grams')]}

bw=json.loads(json.dumps(byname['Black & White Malted Brownie Cookies']))
bw['bakeMinutes']=12
van=[I('Malted Vanilla Dough','Butter',60,'Grams'),I('Malted Vanilla Dough','Dark Brown Sugar',75,'Grams'),I('Malted Vanilla Dough','Granulated Sugar',90,'Grams'),
     I('Malted Vanilla Dough','Eggs',1,'Whole'),I('Malted Vanilla Dough','Vanilla Bean Paste',5,'Milliliters'),I('Malted Vanilla Dough','Flour',60,'Grams'),
     I('Malted Vanilla Dough','Malted Milk Powder',50,'Grams'),I('Malted Vanilla Dough','Baking Powder & Salt',1.5,'Grams')]
bw['ingredients']=[i for i in bw['ingredients'] if i.get('phase')!='Malted Vanilla Dough']+van
bw['notes']=('Vanilla + chocolate (no white chocolate). CHOCOLATE half: melt chocolate with butter; whip eggs and sugars on high about 5 min to a pale ribbon for the crackly top; fold in chocolate, then dry. '
 'VANILLA half: melt the butter; whip egg, both sugars and vanilla bean paste to a pale ribbon; fold in butter, then flour, malted milk powder, baking powder and salt. The extra butter, sugar and malt stand in for the white chocolate that used to give this half its body. '
 'Chill both doughs 20 min; scoop half of each into one ball for a marbled black-and-white drop. Bake at 350°F for 12-13 min until edges set; centers firm up as they cool. Test one sheet first: the vanilla half may spread a little more.'+src)

old=byname['Jam Thumbprint Cookies']
ch={'name':'Cherry Phosphate Shortbread Thumbprints','book':'Your Jam Thumbprint Cookies (flavor ideas from Art of Drink)','bookUrl':'https://www.artofdrink.com/soda/cherry-phosphate','page':'N/A',
 'cookiesPerBatch':36,'refrigerate':'Chill shaped cookies while oven preheats','ovenTemp':'350','bakeMinutes':13,
 'notes':('Built on your proven Jam Thumbprint proportions (egg yolk only, no added liquid, no baking soda) so the wells hold. '
  'Cream butter, sugar and honey; beat in yolk and extracts; mix in flour, cherry powder, baking powder and salt. Roll 1 in. balls, press wells and chill shaped cookies while the oven preheats. '
  'FILLING: simmer sour cherry preserves until thick and jammy, then cool. Stir in acid phosphate and bark infusion off-heat. Fill about 1/2 tsp per cookie. Bake at 350°F for 12-13 min until edges just set. Dust with powdered sugar once cool.'+src.replace('24','36')),
 'ingredients':[
  I('Dough','Butter',12,'Tablespoons',170.2),I('Dough','Granulated Sugar',0.75,'Cups',150),I('Dough','Honey',2,'Tablespoons',42),I('Dough','Egg Yolks',1,'Whole',18),
  I('Dough','Cherry Extract',0.75,'Teaspoons'),I('Dough','Almond Extract',0.25,'Teaspoons'),
  I('Dough','Flour',2.25,'Cups',270),I('Dough','Freeze-Dried Cherry Powder',2,'Tablespoons',8),I('Dough','Baking Powder',1,'Teaspoons',4),I('Dough','Salt',0.5,'Teaspoons',3),
  I('Cherry Phosphate Filling','Sour Cherry Preserves',0.5,'Cups',160),I('Cherry Phosphate Filling','Acid Phosphate Solution',1,'Teaspoons'),
  I('Cherry Phosphate Filling','Wild Cherry Bark Maceration',1,'Teaspoons'),I('Finish','Powdered Sugar',0.25,'Cups',28.4)]}

ms=json.loads(json.dumps(byname["Sarsaparilla Millionaire's Shortbread Bars"]))
ms['name']="Root Beer Float Millionaire's Bars"
ms['ingredients']=[i for i in ms['ingredients'] if i.get('phase')!='Top Finish']
ms['ingredients'].insert(len(ms['ingredients']),I('Sarsaparilla Caramel','Ground Star Anise',0.5,'Grams'))
ms['ingredients']+=[I('Vanilla "Ice Cream" Top','Chocolate, White',100,'Grams'),I('Vanilla "Ice Cream" Top','Vanilla Bean Paste',2.5,'Milliliters'),I('Vanilla "Ice Cream" Top','Flaky Sea Salt',1,'Grams')]
ms['notes']=('Root beer float: root beer caramel under a vanilla "ice cream" layer, with no dark chocolate. Bake pressed shortbread crust 25 min at 350°F. '
 'Cook caramel to 240°F (soft ball); off heat stir in vanilla, sarsaparilla/root beer extract and the pinch of star anise (it rounds out the extract). Pour over cooled crust and let set. '
 'TOP: melt white chocolate with vanilla bean paste and spread very thin, about 2 mm, so it reads as vanilla rather than candy. Add a few flakes of salt before it sets. Cut with a hot knife. '
 'Caramel method: https://cleverpinkpirate.com/root-beer-caramel-recipe/'+src)

lime={'name':'Lime Rickey Drops','book':'Custom (soft sour-cream sugar cookie base)','bookUrl':'','page':'N/A',
 'cookiesPerBatch':24,'refrigerate':'Chill dough 30 min','ovenTemp':'350','bakeMinutes':10,
 'notes':('Soft, cakey, tart lime cookie with a sharp sour glaze, the bright counterpoint in the box. '
  'Rub zest into sugar; cream with butter; beat in egg, sour cream, lime juice and vanilla; mix in dry. Chill 30 min. Scoop 2 Tbsp balls. Bake at 350°F for 9-11 min until just set and not browned, so they stay soft. '
  'GLAZE: whisk powdered sugar, lime juice and citric acid. Dip tops once cool and finish with fresh zest. Mixing the citric acid into the glaze keeps it from weeping and getting sticky when mailed. '
  'Optional: a tiny drop of green gel color in the glaze for Christmas green.'+src),
 'ingredients':[
  I('Dough','Butter',113,'Grams'),I('Dough','Granulated Sugar',150,'Grams'),I('Dough','Lime Zest',3,'Whole'),I('Dough','Eggs',1,'Whole'),
  I('Dough','Sour Cream',120,'Grams'),I('Dough','Lime Juice',15,'Milliliters'),I('Dough','Vanilla Extract',5,'Milliliters'),
  I('Dough','Flour',250,'Grams'),I('Dough','Baking Powder',6,'Grams'),I('Dough','Baking Soda',2.4,'Grams'),I('Dough','Salt',3,'Grams'),
  I('Sour Lime Glaze','Powdered Sugar',120,'Grams'),I('Sour Lime Glaze','Lime Juice',30,'Milliliters'),I('Sour Lime Glaze','Citric Acid',2,'Grams'),I('Sour Lime Glaze','Lime Zest',1,'Whole')]}

rev=[egg,bw,ch,ms,lime]
json.dump({'recipes':rev},open('/home/claude/work/retro-2026-revisions.json','w'),indent=1)
# seed: replace revised, add new; rename bars
seed['recipes']=[r for r in seed['recipes'] if r['name'] not in ('Black & White Malted Brownie Cookies','Cherry Phosphate Shortbread Thumbprints',"Sarsaparilla Millionaire's Shortbread Bars")]+rev
seed['seedVersion']=3
json.dump(seed,open('/home/claude/app/seed.json','w'),separators=(',',':'))
print(len(seed['recipes']))
