import json
U={'g':'Grams','ml':'Milliliters','ea':'Whole','tsp':'Teaspoons'}
R=[
("Egg Cream Carbonated Milk & Dark Chocolate Drops","The Tasty Flavors","https://thetastyflavors.com/milk-cookies-recipe/",11,
 "Soft tender milk cookie base infused with dark chocolate syrup, malt, and cold club soda for an airy egg cream lift. Fold in chilled seltzer right before portioning. Bake 10-12 min.",[
("Butter & Sugar Emulsion","Unsalted Butter (softened)",113,"g"),("Butter & Sugar Emulsion","Granulated Sugar",120,"g"),("Butter & Sugar Emulsion","Dark Brown Sugar",60,"g"),
("Liquid Dairy & Syrup Emulsion","Whole Milk / Sweetened Condensed Milk",60,"ml"),("Liquid Dairy & Syrup Emulsion","U-Bet / Dark Chocolate Syrup",60,"ml"),
("Effervescent Leavening","Club Soda / Seltzer",45,"ml"),("Flavor & Aromatics","Vanilla Extract",5,"ml"),
("Dry Blend & Structure","Flour",280,"g"),("Dry Blend & Structure","Malted Milk Powder",40,"g"),("Dry Blend & Structure","Baking Powder",4,"g"),("Dry Blend & Structure","Salt",3,"g"),
("Inclusions & Baking","Dark Chocolate Chunks (60%)",150,"g")]),
("Black & White Malted Brownie Cookies","Sally's Baking Addiction","https://sallysbakingaddiction.com/brownie-cookies/",None,
 "Melted chocolate + whipped egg/sugar for a crackly top; chill both doughs 20 min and scoop half vanilla, half chocolate into marbled drops.",[
("Malted Dark Chocolate Dough","Chocolate, Bittersweet",113,"g"),("Malted Dark Chocolate Dough","Butter",35,"g"),("Malted Dark Chocolate Dough","Dark Brown Sugar",75,"g"),
("Malted Dark Chocolate Dough","Granulated Sugar",25,"g"),("Malted Dark Chocolate Dough","Eggs",1,"ea"),("Malted Dark Chocolate Dough","Vanilla Bean Paste",2.5,"ml"),
("Malted Dark Chocolate Dough","Flour",47,"g"),("Malted Dark Chocolate Dough","Dutch-Process Cocoa Powder",10,"g"),("Malted Dark Chocolate Dough","Malted Milk Powder",20,"g"),
("Malted Dark Chocolate Dough","Espresso Powder",0.5,"tsp"),("Malted Dark Chocolate Dough","Baking Powder & Salt",1.5,"g"),
("Malted Vanilla Dough","Chocolate, White",113,"g"),("Malted Vanilla Dough","Butter",35,"g"),("Malted Vanilla Dough","Dark Brown Sugar",75,"g"),
("Malted Vanilla Dough","Granulated Sugar",25,"g"),("Malted Vanilla Dough","Eggs",1,"ea"),("Malted Vanilla Dough","Vanilla Bean Paste",5,"ml"),
("Malted Vanilla Dough","Flour",60,"g"),("Malted Vanilla Dough","Malted Milk Powder",30,"g"),("Malted Vanilla Dough","Baking Powder & Salt",1.5,"g")]),
("Coca-Cola Molasses Crinkle Cookies","The Baker Chick","https://www.thebakerchick.com/easy-molasses-crinkle-cookies/",9,
 "Reduce 2 L Mexican Coke to 1.5 cups of syrup (4x) and use it in place of molasses. Roll 1.5-inch balls in sugar; bake 8-10 min.",[
("Crinkle Dough","Vegetable Oil",140,"ml"),("Crinkle Dough","Granulated Sugar",100,"g"),("Crinkle Dough","Dark Brown Sugar",100,"g"),
("Cola Reduction","Reduced Coca-Cola Syrup",60,"ml"),("Crinkle Dough","Eggs",1,"ea"),("Spice & Leavening","Ground Ginger",3,"g"),("Spice & Leavening","Ground Cinnamon",3,"g"),
("Spice & Leavening","Ground Cloves",1.5,"g"),("Crinkle Dough","Vanilla Extract",2.5,"ml"),("Spice & Leavening","Baking Soda",10,"g"),("Crinkle Dough","Flour",270,"g"),
("Coating","Granulated Sugar (for rolling)",100,"g")]),
("Cherry Phosphate Shortbread Thumbprints","Sally's Baking Addiction","https://sallysbakingaddiction.com/lemon-thumbprint-cookies/",None,
 "Thumbprint base with cherry extract & tart juice in place of lemon; chill dough 3 hours, roll in sugar, press wells, fill with wild cherry bark & acid phosphate jam (stir phosphate in off-heat). Cherry phosphate reference: https://www.artofdrink.com/soda/cherry-phosphate",[
("Jam","Sour Cherry Preserves / Puree",200,"g"),("Jam","Wild Cherry Bark Maceration",30,"ml"),("Jam","Acid Phosphate Solution",15,"ml"),("Jam","Granulated Sugar / Pectin",50,"g"),
("Shortbread Dough","Unsalted Butter (softened)",165,"g"),("Shortbread Dough","Granulated Sugar",120,"g"),("Shortbread Dough","Cherry Extract",5,"ml"),
("Shortbread Dough","Sour Cherry Juice",15,"ml"),("Shortbread Dough","Eggs",1,"ea"),("Shortbread Dough","Vanilla Bean Paste",5,"ml"),
("Shortbread Dough","Flour",230,"g"),("Shortbread Dough","Cornstarch",7,"g"),("Shortbread Dough","Salt",2,"g"),("Shortbread Dough","Granulated Sugar (for rolling)",80,"g")]),
("Sarsaparilla Millionaire's Shortbread Bars","Sugar Spun Run","https://sugarspunrun.com/millionaires-shortbread/",25,
 "Bake pressed shortbread crust 25 min at 350°F. Cook caramel to 240°F (soft ball), then stir in vanilla and sarsaparilla extract off-heat (root beer caramel method: https://cleverpinkpirate.com/root-beer-caramel-recipe/). Top with thin white chocolate, dust with powdered sugar, cut into bars.",[
("Shortbread Crust","Unsalted Butter",226,"g"),("Shortbread Crust","Granulated Sugar",70,"g"),("Shortbread Crust","Dark Brown Sugar",70,"g"),("Shortbread Crust","Egg Yolks",1,"ea"),
("Shortbread Crust","Vanilla Bean Paste",5,"ml"),("Shortbread Crust","Flour",280,"g"),("Shortbread Crust","Salt",3,"g"),
("Sarsaparilla Caramel","Brown Sugar",200,"g"),("Sarsaparilla Caramel","Granulated Sugar",200,"g"),("Sarsaparilla Caramel","Butter",226,"g"),
("Sarsaparilla Caramel","Sweetened Condensed Milk",396,"g"),("Sarsaparilla Caramel","Corn Syrup",250,"ml"),("Sarsaparilla Caramel","Heavy Cream",30,"ml"),
("Sarsaparilla Caramel","Vanilla Extract",7.5,"ml"),("Sarsaparilla Caramel","Sarsaparilla / Root Beer Extract",7.5,"ml"),
("Top Finish","Chocolate, White",150,"g"),("Top Finish","Powdered Sugar",50,"g")]),
("Orange Creamsicle Drops","Recipes by Aria","https://recipesbyaria.com/creamsicle-cookies/",11,
 "Rub orange zest into the sugars; fold in white chocolate chips. Bake 10-12 min at 350°F until edges are light golden; drizzle with orange-vanilla glaze once cool.",[
("Creamsicle Dough","Unsalted Butter",113,"g"),("Creamsicle Dough","Granulated Sugar",100,"g"),("Creamsicle Dough","Dark Brown Sugar",100,"g"),("Creamsicle Dough","Eggs",2,"ea"),
("Creamsicle Dough","Vanilla Extract",10,"ml"),("Creamsicle Dough","Orange Extract & Zest",15,"g"),("Creamsicle Dough","Flour",280,"g"),("Creamsicle Dough","Baking Soda",5,"g"),
("Creamsicle Dough","Salt",3,"g"),("Inclusions","White Chocolate Chips",175,"g"),("Glaze","Orange-Vanilla Drizzle",100,"g")]),
]
out=[]
for name,book,url,bake,notes,ings in R:
    rec={'name':name,'book':book,'bookUrl':url,'page':'N/A','cookiesPerBatch':24,'refrigerate':'','ovenTemp':'350','bakeMinutes':bake,
         'notes':notes+' (From the Retro Soda Fountain Cookies Master Plan; base batch = 24 cookies.)','ingredients':[]}
    if 'Thumbprint' in name: rec['refrigerate']='3 hours'
    if 'Brownie' in name: rec['refrigerate']='20 minutes'
    for ph,n,a,u in ings:
        i={'name':n,'amount':a,'unit':U[u],'phase':ph}
        if u=='g': i['grams']=a
        rec['ingredients'].append(i)
    out.append(rec)
json.dump(out,open('/home/claude/data/retro_recipes.json','w'),indent=1)
print(len(out), sum(len(r['ingredients']) for r in out))
