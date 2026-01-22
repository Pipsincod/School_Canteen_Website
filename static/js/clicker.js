'use strict'

function all_action(){
    const hpEl = document.getElementById('id_hp')
    const iqEl = document.getElementById('id_iq')
    const happi_index = document.getElementById('id_happi_index')

    switch (action){
        case "eat":
            if(hpEl)
                hpEl.value = parseInt(hpEl.value, 10) + 5
            break
        case "study":
            if(hpEl)
                iqEl.value = parseInt(iqEl.value, 10) + 1
                happi_indexEl.value = parseInt(happi_indexEl.value, 10) - 20
                break
        case "happi":
            if(hpEl)
                hpEl.value = parseInt(hpEl.value, 10) - 5
                happi_indexEl.value = parseInt(happi_indexEl.value, 10) + 10
            break
        case "sleep":
            if(hpEl)
                hpEl.value = parseInt(hpEl.value, 10) + 5
            break
        default:
            console.error("Unknow action", action)

    }
}

/*
function eat(){
    let hpEl = document.getElementById('hp')
    let hpVal = Number(hpEl.innerHTML)
    hpEl.innerHTML = hpVal + 5
}
function study(){
    let iqEl = document.getElementById('iq')
    let iqVal = Number(iqEl.innerHTML)
    let happiEl = document.getElementById('happi_index')
    let happiVal = Number(happiEl.innerHTML)
    let hpEl = document.getElementById('hp')
    let hpVal = Number(hpEl.innerHTML)
    hpEl.innerHTML = hpVal - 2
    iqEl.innerHTML = hpVal + 1
    happiEl.innerHTML = happiVal - 20
}
function happi(){
    let happiEl = document.getElementById('happi_index')
    let happiVal = Number(happiEl.innerHTML)
    let hpEl = document.getElementById('hp')
    let hpVal = Number(hpEl.innerHTML)
    hpEl.innerHTML = hpVal - 3
    happiEl.innerHTMl = happiVal + 5
}
function sleep(){
    let happiEl = document.getElementById('happi_index')
    let happiVal = Number(happiEl.innerHTML)
    happiEl.innerHTML = happiVal + 10
}
*/