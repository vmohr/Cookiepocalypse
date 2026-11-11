import json
LB=453.592; OZ=28.3495
def G(i,u,g): return {'ingredient':i,'unit':u,'grams':round(g,4)}
def B(i,u,bu,per): return {'ingredient':i,'unit':u,'bulkUnit':bu,'perBulk':round(per,4)}
# King Arthur Ingredient Weight Chart (cup weights as listed; derived spoons = cup/16, /48)
ka=[('Flour','Cups',120),('Flour','Tablespoons',7.5),('Granulated Sugar','Cups',198),('Granulated Sugar','Tablespoons',198/16),
 ('Light Brown Sugar','Cups',213),('Dark Brown Sugar','Cups',213),('Brown Sugar','Cups',213),('Powdered Sugar','Cups',113),
 ('Turbinado Sugar','Cups',180),('Demerara Sugar','Cups',220),('Coconut Palm Sugar','Cups',198),('Maple Sugar','Cups',198),
 ('Butter','Tablespoons',113/8),('Vegetable Shortening','Cups',184),('Vegetable Oil','Cups',198),
 ('Baking Powder','Teaspoons',4),('Baking Soda','Teaspoons',6),('Salt','Teaspoons',6),('Salt','Tablespoons',18),
 ('Cocoa Powder','Cups',84),('Dutch-Process Cocoa Powder','Cups',84),('Cornstarch','Cups',112),('Cornstarch','Teaspoons',112/48),
 ('Milk Powder','Cups',112),('Nonfat Milk Powder','Cups',112),('Malted Milk Powder','Cups',140),
 ('Molasses','Cups',340),('Molasses','Tablespoons',340/16),('Honey','Tablespoons',21),('Corn Syrup','Cups',312),
 ('Maple Syrup','Cups',312),('Heavy Cream','Cups',227),('Milk','Cups',227),('Milk','Tablespoons',227/16),('Whole Milk','Cups',227),
 ('Sour Cream','Cups',227),('Sweetened Condensed Milk','Cups',312),
 ('Eggs','Whole',50),('Egg Whites','Whole',35),('Egg Yolks','Whole',14),
 ('Vanilla Extract','Tablespoons',14),('Vanilla Extract','Teaspoons',14/3),('Espresso Powder','Teaspoons',7/3),
 ('Old Fashioned Rolled Oats','Cups',89),('Pecans','Cups',105),('Toasted Walnuts','Cups',113),('Almonds','Cups',142),('Peanuts','Cups',142),
 ('Peanut Butter','Cups',270),('Mini Chocolate Chips','Cups',177),('Shredded Coconut','Cups',85),('Dried Cherries','Cups',142),
 ('Dried Cranberries','Cups',114),('Mini Marshmallows','Cups',43),('Sour Cherry Preserves','Cups',340),('Jam','Cups',340),
 ('Lemon Juice','Tablespoons',14),('Lime Juice','Tablespoons',14),('Cornmeal','Cups',138),('Masa Harina','Cups',93),
 ('Semolina Flour','Cups',163),('Almond Flour','Cups',96),('Whole Wheat Flour','Cups',113),('Water','Cups',227),
 # metric (ml) entries use true density
 ('Water','Milliliters',1.0),('Heavy Cream','Milliliters',0.99),
 # molasses-strength Coca-Cola syrup behaves like molasses by volume
 ('Reduced Coca-Cola Syrup','Cups',340),('Reduced Coca-Cola Syrup','Milliliters',1.40),
 # wild cherry syrup components
 ('Vegetable Glycerin','Teaspoons',6.3),
 # egg parts written as units in older recipes
 ('Eggs','Yolk',14),('Eggs','Whites',35),('Sugar','Cups',198),
 # USDA household measures (King Arthur doesn't list spices)
 ('Ground Cloves','Teaspoons',2.1),('Cloves','Teaspoons',2.1),('Ground Nutmeg','Teaspoons',2.2),('Nutmeg','Teaspoons',2.2),
 ('Ground Allspice','Teaspoons',1.9),('Ground Cardamom','Teaspoons',2.0),('Ground Coriander','Teaspoons',1.8),
 ('Black Pepper','Teaspoons',2.3),('Anise Seed','Teaspoons',2.1),('Ginger','Tablespoons',5.4),('Ground Cinnamon','Teaspoons',2.6),
 # extracts and spirits (vanilla per King Arthur; others ~ same density)
 ('Peppermint Extract','Teaspoons',14/3),('Anise Extract','Teaspoons',14/3),('Vanilla','Teaspoons',14/3),
 ('Dark Rum','Teaspoons',4.6),('Kirschwasser','Teaspoons',4.6),('Rum','Cups',223),('Club Soda / Seltzer','Milliliters',1.0),('Tart Cherry Juice','Teaspoons',5.2),('Acid Phosphate Solution','Teaspoons',5.4),
]
gram=[G(*x) for x in ka]
coke_g_per_l = 39/0.355 / (1-0.2187)   # 109.9 g sugar per L Coke -> syrup at molasses' 21.9% water
bulk=[B('Reduced Coca-Cola Syrup','Grams','Liters of Coca-Cola',coke_g_per_l),
      B('Reduced Coca-Cola Syrup','Milliliters','Liters of Coca-Cola',coke_g_per_l/1.40),
      B('Wild Cherry Bark','Grams','Ounces',OZ), B('Vegetable Glycerin','Grams','Fluid Ounces',37.3),
      B('Tart Cherry Juice','Grams','Fluid Ounces',30.8), B('Acid Phosphate Solution','Teaspoons','Fluid Ounces',6),
      ]
per_batch=1/12   # each thumbprint batch uses 2 Tbsp (1 fl oz) of the 12-fl-oz Art of Drink syrup
syr='Wild Cherry Syrup (make all at once)'
thumb_edits=[
 {'recipe':'Cherry Phosphate Shortbread Thumbprints','find':{'name':'Wild Cherry Bark Maceration'},'replaceWith':[
   {'name':'Wild Cherry Bark','amount':round(OZ*per_batch,2),'unit':'Grams','grams':round(OZ*per_batch,2),'phase':syr},
   {'name':'Vegetable Glycerin','amount':0.5,'unit':'Teaspoons','grams':3.15,'phase':syr},
   {'name':'Water','amount':20,'unit':'Grams','grams':20,'phase':syr},
   {'name':'Tart Cherry Juice','amount':2,'unit':'Teaspoons','grams':10.4,'phase':syr},
   {'name':'Granulated Sugar','amount':round(10*OZ*per_batch,1),'unit':'Grams','grams':round(10*OZ*per_batch,1),'phase':syr}]},
 {'recipe':'Cherry Phosphate Shortbread Thumbprints','find':{'name':'Acid Phosphate Solution'},'replaceWith':[
   {'name':'Acid Phosphate Solution','amount':0.67,'unit':'Teaspoons','grams':3.6,'phase':'Cherry Phosphate Filling'}]},
 {'recipe':'Cherry Phosphate Shortbread Thumbprints','find':{'name':'Egg Yolks'},'replaceWith':[{'name':'Egg Yolks','amount':1,'unit':'Whole','grams':14,'phase':'Dough'}]},
 {'recipe':'Coca-Cola Molasses Crinkle Cookies','find':{'name':'Reduced Coca-Cola Syrup'},'replaceWith':[
   {'name':'Reduced Coca-Cola Syrup','amount':0.25,'unit':'Cups','grams':85,'phase':'Cola Reduction'}]},
]
notes=[
 {'recipe':'Cherry Phosphate Shortbread Thumbprints','notes':(
  'Built on your proven Jam Thumbprint proportions (egg yolk only, no added liquid, no baking soda) so the wells hold. '
  'Cream butter, sugar and honey; beat in yolk and extracts; mix in flour, cherry powder, baking powder and salt. Roll 1 in. balls, press wells, chill shaped cookies while the oven preheats. '
  'WILD CHERRY SYRUP (Art of Drink, https://www.artofdrink.com/soda/cherry-phosphate): make it in one batch. The full recipe uses 1 oz bark, 1 fl oz glycerin, 4 fl oz water, a second 4 fl oz warm water, 4 fl oz cherry juice and 10 oz sugar, and makes 12 fl oz. '
  'Mix glycerin with the first 4 oz water, pour over the bark, macerate 24 h, then strain. Add the warm water to the bark for 1 h, strain, and combine. Add cherry juice, top up with water to 12 fl oz, and dissolve the sugar without heat. '
  'Each batch of cookies uses 2 Tbsp (1 fl oz) of syrup; 1/3 of the recipe covers 4 batches. '
  'FILLING per batch: simmer the preserves with 2 Tbsp syrup back to a thick jam, then cool. Off heat stir in 2/3 tsp acid phosphate, the drink ratio of 1 tsp per 1 1/2 oz syrup; add more to taste for extra tang. '
  'Fill about 1/2 tsp per cookie. Bake at 350°F for 12-13 min until edges just set. Dust with powdered sugar once cool. (Retro Soda Fountain 2026; base batch = 36.)')},
 {'recipe':'Coca-Cola Molasses Crinkle Cookies','notes':(
  'MOLASSES-STRENGTH COLA SYRUP: reduce Coca-Cola (Mexican, cane sugar) until it has about the same water content as molasses (~22%). '
  'Coke has 39 g sugar per 355 ml (~110 g per liter), so each liter reduces to about 141 g of syrup (~100 ml, a scant 1/2 cup). '
  'Method: weigh your empty pot, simmer flat Coke, and keep reducing until the contents weigh 141 g per liter you started with (2 L -> ~282 g). Near the end it will be bubbling around 225°F; trust the scale over the thermometer. '
  "Coke's phosphoric acid inverts some of the sugar as it cooks, which helps keep the syrup from crystallizing, like molasses. Swap it 1:1 by weight for molasses: 85 g (1/4 cup) per batch. "
  'Then whisk oil and sugars, add syrup, egg and vanilla, mix in dry, roll 1.5 in. balls in sugar, and bake at 350°F for 8-10 min. (Retro Soda Fountain 2026; base batch = 24.)')},
]
patch={'id':'2026-11-weights','ingredientEdits':thumb_edits,'gram':gram,'bulk':bulk,'recalcBulk':True,'syncWeights':True,
 'splits':[{'name':'Light Brown Sugar','into':[{'name':'Dark Brown Sugar','share':0.5},{'name':'Granulated Sugar','share':0.5}]}],
 'removeSubstitutions':['Light Brown Sugar'],'notes':notes,'settings':{'kosherSaltGPerTsp':16/3}}
json.dump(patch,open('/home/claude/work/patch-2026-11-weights.json','w'),indent=1)
print('coke syrup g per liter: %.1f; ml per liter: %.0f; per batch L: %.2f' % (coke_g_per_l, coke_g_per_l/1.4, 85/coke_g_per_l))
