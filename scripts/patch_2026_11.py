import json
LB=453.592; OZ=28.3495; FLOZ=29.5735
def G(i,u,g): return {'ingredient':i,'unit':u,'grams':g}
def B(i,u,bu,per): return {'ingredient':i,'unit':u,'bulkUnit':bu,'perBulk':round(per,4)}
gram=[
 G('Baking Soda','Teaspoons',4.8),        # keep your sheet's value; removes the 6.67 duplicate
 G('Salt','Tablespoons',18),
 G('Light Brown Sugar','Cups',200), G('Dark Brown Sugar','Cups',200), G('Brown Sugar','Cups',200),  # your sheet's convention
 G('Eggs','Whole',54), G('Egg Whites','Whole',36), G('Egg Yolks','Whole',18),
 G('Almond Extract','Teaspoons',4.5), G('Cherry Extract','Teaspoons',4.5),
 G('Vanilla Extract','Milliliters',0.95), G('Vanilla Bean Paste','Milliliters',1.2),
 G('Sarsaparilla / Root Beer Extract','Milliliters',0.95),
 G('Whole Milk','Milliliters',1.03), G('Heavy Cream','Milliliters',0.91), G('Lime Juice','Milliliters',1.0),
 G('Vegetable Oil','Milliliters',0.92), G('Corn Syrup','Milliliters',1.38),
 G('Lime Zest','Whole',2), G('Sour Cherry Preserves','Cups',340), G('Freeze-Dried Cherry Powder','Tablespoons',4),
 G('Espresso Powder','Teaspoons',2.3), G('Honey','Tablespoons',21),
]
# Bulk: plain weights (Pounds / Ounces / Fluid Ounces), eggs by the dozen
bulk=[]
for n in ['Flour','Granulated Sugar','Dark Brown Sugar','Light Brown Sugar','Powdered Sugar','Butter']:
    bulk.append(B(n,'Grams','Pounds',LB))
for n in ['Chocolate, Bittersweet','Chocolate, White','Dutch-Process Cocoa Powder','Malted Milk Powder','Nonfat Milk Powder','Popping Candy (unflavored)',
          'Sour Cream','Vegetable Shortening','Sweetened Condensed Milk','Salt','Baking Powder','Baking Soda','Citric Acid','Ground Ginger','Ground Cinnamon',
          'Ground Cloves','Ground Star Anise','Flaky Sea Salt']:
    bulk.append(B(n,'Grams','Ounces',OZ))
bulk+=[
 B('Flour','Cups','Pounds',LB/120), B('Granulated Sugar','Cups','Pounds',LB/200), B('Powdered Sugar','Cups','Pounds',LB/113.5),
 B('Light Brown Sugar','Cups','Pounds',LB/200), B('Dark Brown Sugar','Cups','Pounds',LB/200), B('Brown Sugar','Cups','Pounds',LB/200),
 B('Butter','Tablespoons','Pounds',32),
 B('Salt','Teaspoons','Ounces',OZ/6), B('Baking Powder','Teaspoons','Ounces',OZ/4), B('Baking Soda','Teaspoons','Ounces',OZ/4.8),
 B('Honey','Tablespoons','Ounces',OZ/21), B('Sour Cherry Preserves','Cups','Ounces',OZ/340), B('Freeze-Dried Cherry Powder','Tablespoons','Ounces',OZ/4),
 B('Espresso Powder','Teaspoons','Ounces',OZ/2.3),
 B('Eggs','Whole','Dozen',12), B('Egg Yolks','Whole','Eggs',1), B('Egg Whites','Whole','Eggs',1),
 B('Whole Milk','Milliliters','Fluid Ounces',FLOZ), B('Heavy Cream','Milliliters','Fluid Ounces',FLOZ), B('Corn Syrup','Milliliters','Fluid Ounces',FLOZ),
 B('Vegetable Oil','Milliliters','Fluid Ounces',FLOZ), B('Vanilla Extract','Milliliters','Fluid Ounces',FLOZ), B('Vanilla Bean Paste','Milliliters','Fluid Ounces',FLOZ),
 B('Sarsaparilla / Root Beer Extract','Milliliters','Fluid Ounces',FLOZ),
 B('Vanilla Extract','Teaspoons','Fluid Ounces',6), B('Almond Extract','Teaspoons','Fluid Ounces',6), B('Cherry Extract','Teaspoons','Fluid Ounces',6),
 B('Acid Phosphate Solution','Teaspoons','Fluid Ounces',6), B('Wild Cherry Bark Maceration','Teaspoons','Fluid Ounces',6),
 B('Reduced Coca-Cola Syrup','Milliliters','Liters of Coca-Cola',355/2),   # 2 L reduces to ~1.5 cups (355 ml)
 B('Lime Zest','Whole','Limes',1), B('Lime Juice','Milliliters','Limes',30),
 # corrections to flagged factors (A per B, from the gram table)
 B('Mini Marshmallows','Cups','Ounces',OZ/52), B('Pecans','Cups','Ounces',OZ/114), B('Dried Cherries','Cups','Ounces',OZ/142),
 B('Peanut Butter','Cups','Ounces',OZ/270), B('Mini Chocolate Chips','Cups','Ounces',OZ/189.39), B('Cinnamon','Teaspoons','Ounces',OZ/2.667),
]
patch={'id':'2026-11-conversions','renames':[
  {'field':'unit','from':['Teaspoon'],'to':'Teaspoons'},
  {'field':'name','from':['Egg'],'to':'Eggs'},
  {'field':'name','from':['Fresh ginger'],'to':'Fresh Ginger'},
  {'field':'name','from':['Ground Clove'],'to':'Ground Cloves'},
  {'field':'name','from':['Unsalted Butter','Unsalted Butter (softened)'],'to':'Butter'},
  {'field':'name','from':['Granulated Sugar (for rolling)'],'to':'Granulated Sugar'}],
 'ingredientEdits':[
  {'recipe':"Root Beer Float Millionaire's Bars",'find':{'name':'Brown Sugar','unit':'Grams'},'replaceWith':[{'name':'Light Brown Sugar','amount':200,'unit':'Grams','grams':200}]},
  {'recipe':'Black & White Malted Brownie Cookies','find':{'name':'Baking Powder & Salt'},'replaceWith':[
     {'name':'Baking Powder','amount':1,'unit':'Grams','grams':1},{'name':'Salt','amount':0.5,'unit':'Grams','grams':0.5}]},
  {'recipe':'Cherry Phosphate Shortbread Thumbprints','find':{'name':'Sour Cherry Preserves','unit':'Cups'},'replaceWith':[{'name':'Sour Cherry Preserves','amount':0.5,'unit':'Cups','grams':170}]}],
 'gram':gram,'bulk':bulk,
 'substitutions':[{'ingredient':'Light Brown Sugar','buyAs':'Dark Brown Sugar','share':0.5},{'ingredient':'Light Brown Sugar','buyAs':'Granulated Sugar','share':0.5}],
 'settings':{'kosherSaltGPerTsp':4.8}}
json.dump(patch,open('/home/claude/work/patch-2026-11.json','w'),indent=1)
print(len(gram),'gram',len(bulk),'bulk')
