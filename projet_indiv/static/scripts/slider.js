var slider = document.getElementById('range');


noUiSlider.create(slider, {
    start: [ 0, 100], // Handle start position
    step: 1, // Slider moves in increments of '10'
    margin: 1, // Handles must be more than '20' apart
    connect: true, // Display a colored bar between the handles
    behaviour: 'tap-drag', // Move handle on tap, bar is draggable
    tooltips: [true, true], //to see the values
    range: { // Slider can select '0' to '100'
        'min': 0,
        'max': 100
    },
});

var minProgressInput = document.getElementById('minProgress'),
    maxProgressInput = document.getElementById('maxProgress');

// When the slider value changes, update the input and span
slider.noUiSlider.on('update', function( values, handle ) {
    if ( handle ) {
        maxProgressInput.value = values[handle];
    } else {
        minProgressInput.value = values[handle];
    }
});

minProgressInput.addEventListener('change', function(){
    slider.noUiSlider.set([null, this.value]);
});

maxProgressInput.addEventListener('change', function(){
    slider.noUiSlider.set([null, this.value]);
});

