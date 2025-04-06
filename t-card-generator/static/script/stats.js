class Pokemon{
    VITA_VALUE = 5;
//
    constructor() {
        this.lvl = 5;
        this.shiny = false;
        this.pv = 0;
        this.pvAdd = 0;
        this.atk = 0;
        this.atkAdd = 0;
        this.def = 0;
        this.defAdd = 0;
        this.atkSpe = 0;
        this.atkSpeAdd = 0;
        this.defSpe = 0;
        this.defSpeAdd = 0;
        this.vit = 0;
        this.vitAdd = 0;
        this.pvPlus = 0;
        this.prot = 0;
        this.fer = 0;
        this.calcium = 0;
        this.zinc = 0;
        this.carbone = 0;
    }

    totalSpend() {
        return this.pvAdd + this.atkAdd + this.defAdd + this.atkSpeAdd + this.defSpeAdd + this.vitAdd;
    }

    totalPv() {
        return this.pv + this.pvAdd + this.getPvPlusRealValue();
    }

    totalAtk() {
        return this.atk + this.atkAdd + this.getProtRealValue();
    }

    totalDef() {
        return this.def + this.defAdd + this.getFerRealValue();
    }

    totalAtkSpe() {
        return this.atkSpe + this.atkSpeAdd + this.getCalciumRealValue();
    }

    totalDefSpe() {
        return this.defSpe + this.defSpeAdd + this.getZincRealValue();
    }

    totalVit() {
        return this.vit + this.vitAdd + this.getCarboneRealValue();
    }

    getPointValue() {
        return this.shiny ? 9 : 8;
    }

    getWinLvl() {
        return this.lvl - 5;
    }

    getMaxPoints() {
        return this.getWinLvl() * this.getPointValue();
    }

    getVitaminesNumberUsed() {
        return this.pvPlus + this.prot + this.fer + this.calcium + this.zinc + this.carbone;
    }

    getPvPlusRealValue() {
        return this.pvPlus * this.VITA_VALUE;
    }

    getProtRealValue() {
        return this.prot * this.VITA_VALUE;
    }

    getFerRealValue() {
        return this.fer * this.VITA_VALUE;
    }

    getCalciumRealValue() {
        return this.calcium * this.VITA_VALUE;
    }

    getZincRealValue() {
        return this.zinc * this.VITA_VALUE;
    }

    getCarboneRealValue() {
        return this.carbone * this.VITA_VALUE;
    }
}
//
//
// // Pokémon
// const POKEMON_BASE = {
//     "Kero": {
//         "pv": 39,
//         "atk": 52,
//         "def": 43,
//         "atkSpe": 60,
//         "defSpe": 50,
//         "vit": 65
//     },
//     "Nido": {
//         "pv": 61,
//         "atk": 72,
//         "def": 57,
//         "atkSpe": 55,
//         "defSpe": 55,
//         "vit": 65
//     },
//     "Piafabec": {
//         "pv": 40,
//         "atk": 60,
//         "def": 30,
//         "atkSpe": 31,
//         "defSpe": 31,
//         "vit": 70
//     },
//     "Boustiflor": {
//         "pv": 50,
//         "atk": 75,
//         "def": 35,
//         "atkSpe": 70,
//         "defSpe": 30,
//         "vit": 40
//     },
//     "Diabolo": {
//         "pv": 35,
//         "atk": 55,
//         "def": 40,
//         "atkSpe": 50,
//         "defSpe": 50,
//         "vit": 90
//     },
//     "Draby": {
//         "pv": 45,
//         "atk": 75,
//         "def": 60,
//         "atkSpe": 40,
//         "defSpe": 30,
//         "vit": 50
//     },
//     "Spiritomb": {
//         "pv": 50,
//         "atk": 92,
//         "def": 108,
//         "atkSpe": 92,
//         "defSpe": 108,
//         "vit": 35
//     },
//     "Wattouat": {
//         "pv": 55,
//         "atk": 40,
//         "def": 40,
//         "atkSpe": 65,
//         "defSpe": 45,
//         "vit": 35
//     },
//     "Embrylex": {
//         "pv": 50,
//         "atk": 64,
//         "def": 50,
//         "atkSpe": 45,
//         "defSpe": 50,
//         "vit": 41
//     },
//     "Minisange": {
//         "pv": 38,
//         "atk": 47,
//         "def": 35,
//         "atkSpe": 33,
//         "defSpe": 35,
//         "vit": 57
//     },
//     "Monorpale": {
//         "pv": 45,
//         "atk": 80,
//         "def": 100,
//         "atkSpe": 35,
//         "defSpe": 37,
//         "vit": 28
//     },
//     "Fantominus": {
//         "pv": 30,
//         "atk": 35,
//         "def": 30,
//         "atkSpe": 100,
//         "defSpe": 35,
//         "vit": 80
//     },
//     "Grenousse": {
//         "pv": 41,
//         "atk": 56,
//         "def": 40,
//         "atkSpe": 62,
//         "defSpe": 44,
//         "vit": 71
//     },
//     "Rattata": {
//         "pv": 30,
//         "atk": 56,
//         "def": 35,
//         "atkSpe": 25,
//         "defSpe": 35,
//         "vit": 72
//     },
// };
//
// Inputs
const cbShiney = document.getElementById('cbShiney');
const lvlInput = document.getElementById('lvl');
const pvInput = document.getElementById('pv');
const atkInput = document.getElementById('atk');
const defInput = document.getElementById('defense');
const atkSpeInput = document.getElementById('atk_spe');
const defSpeInput = document.getElementById('defense_spe');
const vitInput = document.getElementById('speed');
// const removePvPlus = document.getElementById('remove-pvplus');
const addPvPlus = document.getElementById('hp_up');
// const removeProt = document.getElementById('remove-prot');
const addProt = document.getElementById('protein');
// const removeFer = document.getElementById('remove-fer');
const addFer = document.getElementById('iron');
// const removeCalcium = document.getElementById('remove-calcium');
const addCalcium = document.getElementById('calcium');
// const removeZinc = document.getElementById('remove-zinc');
const addZinc = document.getElementById('zinc');
// const removeCarbone = document.getElementById('remove-carbone');
const addCarbone = document.getElementById('carbos');
//
// // Points distribués
// const pvSpend = document.getElementById('hp_up');
// const atkSpend = document.getElementById('atkSpend');
// const defSpend = document.getElementById('defSpend');
// const atkSpeSpend = document.getElementById('atkSpeSpend');
// const defSpeSpend = document.getElementById('defSpeSpend');
// const vitSpend = document.getElementById('vitSpend');
// const winLvl = document.getElementsByClassName('winLvl');
// const pvPlusSpend = document.getElementById('pvPlusSpend');
// const protSpend = document.getElementById('protSpend');
// const ferSpend = document.getElementById('ferSpend');
// const calciumSpend = document.getElementById('calciumSpend');
// const zincSpend = document.getElementById('zincSpend');
// const carboneSpend = document.getElementById('carboneSpend');
const pvPlusReal = document.getElementById('pvPlusReal');
const protReal = document.getElementById('protReal');
const ferReal = document.getElementById('ferReal');
const calciumReal = document.getElementById('calciumReal');
const zincReal = document.getElementById('zincReal');
const carboneReal = document.getElementById('carboneReal');
// const vitaUsed = document.getElementById('vitaUsed');
//
// // Points totals
const pvTot = document.getElementById('pvTot');
const atkTot = document.getElementById('atkTot');
const defTot = document.getElementById('defTot');
const atkSpeTot = document.getElementById('atkSpeTot');
const defSpeTot = document.getElementById('defSpeTot');
const vitTot = document.getElementById('vitTot');
const pointTot = document.getElementById('pointTot');
const vitaTot = document.getElementById('vitaTot');
//
// // Stats de base
const pvBase = document.getElementById('pvBase');
const atkBase = document.getElementById('atkBase');
const defBase = document.getElementById('defBase');
const atkSpeBase = document.getElementById('atkSpeBase');
const defSpeBase = document.getElementById('defSpeBase');
const vitBase = document.getElementById('vitBase');
//
// // Autres
// const copyBtnLuna = document.getElementById('copyBtn-luna');
// const copyBtnLime = document.getElementById('copyBtn-lime');
const saveBtn = document.getElementById('saveBtn');
const totalSpent = document.getElementById('spent');
const lvlPointSpan = document.getElementsByClassName('lvlPoints');
const pointRemaining = document.getElementById('remaining');
// const pokemonName = document.getElementById('pokemonName');
//
// // Globales
let pokemon = null;
//
function changePkmn() {
    pokemon = new Pokemon();

    initStat();
    // displayStats();
    computeSums();
    setLvlStuff();
    initVitaStats();
    updateVitaSpend();
    // updateVitamineStates();
}

function initVitaStats() {
    displayStat(pvPlusReal, pokemon.getPvPlusRealValue());
    displayStat(protReal, pokemon.getProtRealValue());
    displayStat(calciumReal, pokemon.getCalciumRealValue());
    displayStat(zincReal, pokemon.getZincRealValue());
    displayStat(ferReal, pokemon.getFerRealValue());
    displayStat(carboneReal, pokemon.getCarboneRealValue());
}

//
function initStat() {
    // let stats = localStorage.getItem(pokemon.name);

    // if (stats != null) {
    //     stats = JSON.parse(stats);

    console.log(atkBase)
    console.log(atkBase.value)
    console.log(atkBase.content)
    console.log(atkBase.innerText)

    pokemon.lvl = parseInt(lvlInput.value);
    pokemon.shiny = cbShiney.checked;
    pokemon.pv = parseInt(pvBase.innerText);
    pokemon.pvAdd = parseInt(pvInput.value);
    pokemon.atk = parseInt(atkBase.innerText);
    pokemon.atkAdd = parseInt(atkInput.value);
    pokemon.def = parseInt(defBase.innerText);
    pokemon.defAdd = parseInt(defInput.value);
    pokemon.atkSpe = parseInt(atkSpeBase.innerText);
    pokemon.atkSpeAdd = parseInt(atkSpeInput.value);
    pokemon.defSpe = parseInt(defSpeBase.innerText);
    pokemon.defSpeAdd = parseInt(defSpeInput.value);
    pokemon.vit = parseInt(vitBase.innerText);
    pokemon.vitAdd = parseInt(vitInput.value);
    pokemon.pvPlus = parseInt(addPvPlus.value);
    pokemon.prot = parseInt(addProt.value);
    pokemon.fer = parseInt(addFer.value);
    pokemon.calcium = parseInt(addCalcium.value);
    pokemon.zinc = parseInt(addZinc.value);
    pokemon.carbone = parseInt(addCarbone.value);

    console.log(pokemon)
    // }
}
//
// function displayStats() {
//     displayStat(pvBase, pokemon.pv);
//     // displayStat(pvSpend, pokemon.pvAdd);
//     pvInput.value = pokemon.pvAdd;
//     // displayStat(pvPlusSpend, pokemon.pvPlus);
//     displayStat(pvPlusReal, pokemon.getPvPlusRealValue());
//
//     displayStat(atkBase, pokemon.atk);
//     // displayStat(atkSpend, pokemon.atkAdd);
//     atkInput.value = pokemon.atkAdd;
//     // displayStat(protSpend, pokemon.prot);
//     displayStat(protReal, pokemon.getProtRealValue());
//
//     displayStat(defBase, pokemon.def);
//     // displayStat(defSpend, pokemon.defAdd);
//     defInput.value = pokemon.defAdd;
//     // displayStat(ferSpend, pokemon.fer);
//     displayStat(ferReal, pokemon.getFerRealValue());
//
//     displayStat(atkSpeBase, pokemon.atkSpe);
//     // displayStat(atkSpeSpend, pokemon.atkSpeAdd);
//     atkSpeInput.value = pokemon.atkSpeAdd;
//     // displayStat(calciumSpend, pokemon.calcium);
//     displayStat(calciumReal, pokemon.getCalciumRealValue());
//
//     displayStat(defSpeBase, pokemon.defSpe);
//     // displayStat(defSpeSpend, pokemon.defSpeAdd);
//     defSpeInput.value = pokemon.defSpeAdd;
//     // displayStat(zincSpend, pokemon.zinc);
//     displayStat(zincReal, pokemon.getZincRealValue());
//
//     displayStat(vitBase, pokemon.vit);
//     // displayStat(vitSpend, pokemon.vitAdd);
//     vitInput.value = pokemon.vitAdd;
//     // displayStat(carboneSpend, pokemon.carbone);
//     displayStat(carboneReal, pokemon.getCarboneRealValue());
//
//     lvlInput.value = pokemon.lvl;
//     cbShiney.checked = pokemon.shiny;
// }
//
function displayStat(spans, value) {
    spans.textContent = value;
}
//
function computeSums() {
    displayStat(pvTot, pokemon.totalPv());
    displayStat(atkTot, pokemon.totalAtk());
    displayStat(defTot, pokemon.totalDef());
    displayStat(atkSpeTot, pokemon.totalAtkSpe());
    displayStat(defSpeTot, pokemon.totalDefSpe());
    displayStat(vitTot, pokemon.totalVit());
}
//
// function saveStats() {
//     localStorage.setItem(pokemon.name, JSON.stringify(pokemon));
// }
//
function setLvlStuff() {
//     displayStat(lvlPointSpan, pokemon.getPointValue());
//     displayStat(winLvl, pokemon.getWinLvl());
    displayStat(pointTot, pokemon.getMaxPoints());
//
    updatePointSpend();
}
//
function updatePointSpend() {
    totalSpent.textContent = pokemon.totalSpend();
    pointRemaining.textContent = pokemon.getMaxPoints() - pokemon.totalSpend();

    toggleCopyBtnState();
}

function updateVitaSpend() {
    vitaTot.textContent = pokemon.getVitaminesNumberUsed();

    toggleCopyBtnState();
}
//
function toggleCopyBtnState() {
    const totalSpend = pokemon.totalSpend();
    const maxPoints = pokemon.getMaxPoints();
    const vitaSpend = pokemon.getVitaminesNumberUsed();

    let pointOK = false;
    let vitaOK = false;

    if (totalSpend > maxPoints) {
        totalSpent.style.color = "red";
        pointOK = false;
        //saveBtn.setAttribute('disabled', 'true')
        // copyBtnLuna.setAttribute('disabled', true);
        // copyBtnLime.setAttribute('disabled', true);
    } else if (totalSpend === maxPoints) {
        totalSpent.style.color = "green";
        pointOK = true;
        // saveBtn.removeAttribute('disabled');
        // copyBtnLuna.removeAttribute('disabled');
        // copyBtnLime.removeAttribute('disabled');
    } else {
        totalSpent.style.color = "orange";
        pointOK = true;
        // saveBtn.removeAttribute('disabled');
        // copyBtnLuna.removeAttribute('disabled');
        // copyBtnLime.removeAttribute('disabled');
    }

    if (vitaSpend > 10) {
        vitaTot.style.color = "red";
        vitaOK = false;
        //saveBtn.setAttribute('disabled', 'true')
        // copyBtnLuna.setAttribute('disabled', true);
        // copyBtnLime.setAttribute('disabled', true);
    } else {
        vitaTot.style.color = "green";
        vitaOK = true;
        // saveBtn.removeAttribute('disabled');
        // copyBtnLuna.removeAttribute('disabled');
        // copyBtnLime.removeAttribute('disabled');
    }

    if (pointOK && vitaOK) {
        saveBtn.removeAttribute('disabled');
    } else {
        saveBtn.setAttribute('disabled', 'true')
    }
}
//
// function copyFunction(perso) {
//     const copyText = document.getElementById(`myInput-${perso}`).textContent;
//     const textArea = document.createElement('textarea');
//     textArea.textContent = copyText;
//     document.body.append(textArea);
//     textArea.select();
//     document.execCommand("copy");
// }
//
// function togglePokemonShiny() {
//     pokemon.shiny = cbShiney.checked;
//     setLvlStuff();
// }
//
// function changeLvl() {
//     pokemon.lvl = lvlInput.value;
//     setLvlStuff();
// }
//
function changeStat(stat) {
    switch (stat) {
        case "pv":
            pokemon.pvAdd = isNaN(parseInt(pvInput.value)) ? 0 : parseInt(pvInput.value);
            // displayStat(pvSpend, pokemon.pvAdd);
            break;
        case "atk":
            pokemon.atkAdd = isNaN(parseInt(atkInput.value)) ? 0 : parseInt(atkInput.value);
            // displayStat(atkSpend, pokemon.atkAdd);
            break;
        case "def":
            pokemon.defAdd = isNaN(parseInt(defInput.value)) ? 0 : parseInt(defInput.value);
            // displayStat(defSpend, pokemon.defAdd);
            break;
        case "atk_spe":
            pokemon.atkSpeAdd = isNaN(parseInt(atkSpeInput.value)) ? 0 : parseInt(atkSpeInput.value);
            // displayStat(atkSpeSpend, pokemon.atkSpeAdd);
            break;
        case "defense_spe":
            pokemon.defSpeAdd = isNaN(parseInt(defSpeInput.value)) ? 0 : parseInt(defSpeInput.value);
            // displayStat(defSpeSpend, pokemon.defSpeAdd);
            break;
        case "vit":
            pokemon.vitAdd = isNaN(parseInt(vitInput.value)) ? 0 : parseInt(vitInput.value);
            // displayStat(vitSpend, pokemon.vitAdd);
            break;
        case "hp_plus":
            pokemon.pvPlus = isNaN(parseInt(addPvPlus.value)) ? 0 : parseInt(addPvPlus.value);
            displayStat(pvPlusReal, pokemon.getPvPlusRealValue());
            break;
        case "protein":
            pokemon.prot = isNaN(parseInt(addProt.value)) ? 0 : parseInt(addProt.value);
            displayStat(protReal, pokemon.getProtRealValue());
            break;
        case "calcium":
            pokemon.calcium = isNaN(parseInt(addCalcium.value)) ? 0 : parseInt(addCalcium.value);
            displayStat(calciumReal, pokemon.getCalciumRealValue());
            break;
        case "iron":
            pokemon.fer = isNaN(parseInt(addFer.value)) ? 0 : parseInt(addFer.value);
            displayStat(ferReal, pokemon.getFerRealValue());
            break;
        case "zinc":
            pokemon.zinc = isNaN(parseInt(addZinc.value)) ? 0 : parseInt(addZinc.value);
            displayStat(zincReal, pokemon.getZincRealValue());
            break;
        case "carbos":
            pokemon.carbone = isNaN(parseInt(addCarbone.value)) ? 0 : parseInt(addCarbone.value);
            displayStat(carboneReal, pokemon.getCarboneRealValue());
            break;
        default:
            console.log(stat);
            break;
    }

    console.log(pokemon)

    computeSums();
    updatePointSpend();
    updateVitaSpend();
}

// function updateVitaSpend() {
//
// }
//
// function updateVitamineStates() {
//     addPvPlus.removeAttribute('disabled');
//     addProt.removeAttribute('disabled');
//     addFer.removeAttribute('disabled');
//     addCalcium.removeAttribute('disabled');
//     addZinc.removeAttribute('disabled');
//     addCarbone.removeAttribute('disabled');
//     removePvPlus.removeAttribute('disabled');
//     removeProt.removeAttribute('disabled');
//     removeFer.removeAttribute('disabled');
//     removeCalcium.removeAttribute('disabled');
//     removeZinc.removeAttribute('disabled');
//     removeCarbone.removeAttribute('disabled');
//
//     if (pokemon.pvPlus === 0) {
//         removePvPlus.setAttribute('disabled', true);
//     }
//     if (pokemon.prot === 0) {
//         removeProt.setAttribute('disabled', true);
//     }
//     if (pokemon.fer === 0) {
//         removeFer.setAttribute('disabled', true);
//     }
//     if (pokemon.calcium === 0) {
//         removeCalcium.setAttribute('disabled', true);
//     }
//     if (pokemon.zinc === 0) {
//         removeZinc.setAttribute('disabled', true);
//     }
//     if (pokemon.carbone === 0) {
//         removeCarbone.setAttribute('disabled', true);
//     }
//
//     if (pokemon.getVitaminesNumberUsed() === 10) {
//         addPvPlus.setAttribute('disabled', true);
//         addProt.setAttribute('disabled', true);
//         addFer.setAttribute('disabled', true);
//         addCalcium.setAttribute('disabled', true);
//         addZinc.setAttribute('disabled', true);
//         addCarbone.setAttribute('disabled', true);
//     }
//
//     displayStat(vitaTot, pokemon.getVitaminesNumberUsed());
//     displayVitaUsed();
// }
//
// function displayVitaUsed() {
//     const boosts = [];
//     if (pokemon.pvPlus !== 0) {
//         boosts.push(`${pokemon.pvPlus} PV`)
//     }
//     if (pokemon.prot !== 0) {
//         boosts.push(`${pokemon.prot} P`)
//     }
//     if (pokemon.fer !== 0) {
//         boosts.push(`${pokemon.fer} F`)
//     }
//     if (pokemon.calcium !== 0) {
//         boosts.push(`${pokemon.calcium} Cal`)
//     }
//     if (pokemon.zinc !== 0) {
//         boosts.push(`${pokemon.zinc} Z`)
//     }
//     if (pokemon.carbone !== 0) {
//         boosts.push(`${pokemon.carbone} Car`)
//     }
//
//     const text = boosts.length === 0 ? "Aucun" : boosts.join('/');
//     displayStat(vitaUsed, text);
// }
//
function updateVitamines() {
//     displayStats();
//     updateVitamineStates();
    computeSums();
}
//
// changePkmn(document.getElementById('Kero'));
// document.getElementById('Kero').checked = true;
// copyBtnLuna.addEventListener('click', function() {copyFunction('luna')});
// copyBtnLuna.addEventListener('click', saveStats);
// copyBtnLime.addEventListener('click', function() {copyFunction('lime')});
// copyBtnLime.addEventListener('click', saveStats);
// saveBtn.addEventListener('click', saveStats);
//
// cbShiney.addEventListener('click', togglePokemonShiny);
// lvlInput.addEventListener('keyup', changeLvl);
//
pvInput.addEventListener('change', function() {changeStat("pv")});
atkInput.addEventListener('change', function() {changeStat("atk")});
defInput.addEventListener('change', function() {changeStat("def")});
atkSpeInput.addEventListener('change', function() {changeStat("atk_spe")});
defSpeInput.addEventListener('change', function() {changeStat("defense_spe")});
vitInput.addEventListener('change', function() {changeStat("vit")});
//
// removePvPlus.addEventListener('click', function() {pokemon.pvPlus--; updateVitamines();});
addPvPlus.addEventListener('change', function() {changeStat("hp_plus");});
// removeProt.addEventListener('click', function() {pokemon.prot--; updateVitamines();});
addProt.addEventListener('change', function() {changeStat("protein");});
// removeCalcium.addEventListener('click', function() {pokemon.calcium--; updateVitamines();});
addCalcium.addEventListener('change', function() {changeStat("calcium");});
// removeFer.addEventListener('click', function() {pokemon.fer--; updateVitamines();});
addFer.addEventListener('change', function() {changeStat("iron");});
// removeZinc.addEventListener('change', function() {pokemon.zinc--; updateVitamines();});
addZinc.addEventListener('change', function() {changeStat("zinc");});
// removeCarbone.addEventListener('click', function() {pokemon.carbone--; updateVitamines();});
addCarbone.addEventListener('change', function() {changeStat("carbos");});

window.addEventListener('load', function () {
    changePkmn()
})