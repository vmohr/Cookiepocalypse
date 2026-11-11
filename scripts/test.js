const C=require(process.env.CALC||require('path').join(__dirname,'../src/calc.js'));const fs=require('fs');
const s=C.normalizeState(JSON.parse(fs.readFileSync(process.argv[2])));
const sheet=JSON.parse(fs.readFileSync(process.argv[3]));
console.log('units',C.totalUnits(s));
for(const r of C.planRows(s)) console.log(r.item.recipe,r.batches,r.bakeHours&&r.bakeHours.toFixed(1));
const mine=new Map(C.shoppingList(s,{substitutions:false,merge:false}).map(e=>[C.key(e.name)+'|'+C.key(e.unit),e]));
let bad=0,n=0;
for(const [nm,u,amt,bu,ba] of sheet){ if(amt==null) continue; n++; const m=mine.get(C.key(nm)+'|'+C.key(u));
 if(!m||Math.abs(m.amount-amt)>1e-6||(ba!=null&&ba!==''&&Math.abs((m.bulkAmount??0)-ba)>1e-6)){bad++;console.log('DIFF',nm,u,amt,ba,m&&m.amount,m&&m.bulkAmount);} }
console.log('sheet rows with amounts',n,'mine',mine.size,'diffs',bad);
// round trip CSV
const csv=C.recipesToCSV(s.recipes);const back=C.recipesFromCSV(csv);
console.log("csv roundtrip equal", JSON.stringify(back.map(C.normalizeRecipe))===JSON.stringify(s.recipes.map(C.normalizeRecipe)));
const ch=C.conversionChecks(s);console.log(ch.issues.length,'issues');ch.issues.forEach(i=>console.log(i.severity,i.type,'|',i.title,'|',i.detail));
