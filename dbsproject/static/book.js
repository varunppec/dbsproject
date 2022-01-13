
let lis = [{}]
const form = document.querySelector('form');
const select = document.querySelector('.train');
const start = document.querySelector('.start');
const end = document.querySelector('.end');
const submit = document.querySelector('input');
select.onchange = function() {
    //window.alert("booked");
    const dest = document.querySelector('.start');
    dest.removeAttribute('hidden');
    const startpoint = document.querySelector('#startpoint');
    startpoint.removeAttribute('hidden');
    const name = select.selectedOptions[0].getAttribute('name');
    const starts = document.querySelectorAll('.starts');
    starts.forEach(x => {
        if (x.getAttribute('svalue') == name) {
            x.removeAttribute('hidden');
        }
        else {
            x.setAttribute('hidden',"");
        }
    })
};

start.onchange = function() {
    const svalue = start.selectedOptions[0].getAttribute('svalue');
    const dvalue = start.selectedOptions[0].getAttribute('dvalue');
    const ends = document.querySelectorAll('.ends');
    end.removeAttribute('hidden');
    const endpoint = document.querySelector('#endpoint');
    endpoint.removeAttribute('hidden');
    ends.forEach(x => {
        if (x.getAttribute('svalue') == svalue && x.getAttribute('dvalue') > dvalue) {
            x.removeAttribute('hidden');
        }
        else {
            x.setAttribute('hidden', "");
        }
    })
}

end.onchange = function() {
    while (end.nextElementSibling.id != "submit") {
        end.nextElementSibling.remove();
    }
    const h4 = document.createElement('h4');
    h4.innerText = "No of Passengers";
    const select = document.createElement('select');
    select.classList.add('passengerno');
    select.required = true;
    select.onchange = function() {
        const div = document.querySelector('.seats');
        if (div) {
            div.remove();
        }
        const a = document.querySelector('#seatstext');
        a.remove();
        showSeats(parseInt(select.selectedOptions[0].innerText));
    }
    select.classList.add('no');
    select.name = "no";
    let init = document.createElement('option');
    init.setAttribute('disabled', "");
    init.setAttribute('selected', "");
    init.innerText = "No of passengers";
    select.appendChild(init);
    for (i = 0; i < 4; i++) {
        const option = document.createElement('option');
        option.setAttribute('name', i + 1);
        option.innerText = i + 1;
        select.appendChild(option);
    }
    form.insertBefore(h4, submit);
    form.insertBefore(select, submit);
    showSeats(1);
}

const showSeats = function(no) {
    const h4 = document.createElement('h4');
    h4.innerText = "Passenger seats";
    h4.id = "seatstext";
    const seats = document.createElement('div');
    seats.classList.add('seats');
    for (i = 0; i < no; i++) {
        const select = document.createElement('select');
        select.name = "seat" + (i + 1)
        select.required = true;
        select.classList.add('pass' + i + 1);
        seats.append(select);
        const init = document.createElement('option');
        init.innerText = "Passenger " + (i + 1);
        init.setAttribute('disabled',"");
        init.setAttribute("selected", "");
        select.appendChild(init);
        for (j = 0; j < 20; j++) {
            const option = document.createElement('option');
            option.innerText = j + 1;
            select.append(option);
        }
    }
    form.insertBefore(h4, submit);
    form.insertBefore(seats, submit);
}


