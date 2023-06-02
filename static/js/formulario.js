// Obtener las opciones de tipo de cirugía
fetch('/tipos_cirugia')
    .then(response => response.json())
    .then(data => {
        const tipoCirugiaSelect = document.getElementById('tipo-cirugia-list');
        data.tipos_cirugia.forEach(tipoCirugia => {
            const option = document.createElement('option');
            option.value = tipoCirugia;
            tipoCirugiaSelect.appendChild(option);
        });

        // Configurar Autocomplete para el campo "Tipo de Cirugía"
        $('input[data-list]').each(function () {
            const availableTags = $('#' + $(this).attr("data-list")).find('option').map(function () {
                return this.value;
            }).get();

            $(this).autocomplete({
                source: availableTags
            }).on('focus', function () {
                $(this).autocomplete('search', ' ');
            }).on('search', function () {
                if ($(this).val() === '') {
                    $(this).autocomplete('search', ' ');
                }
            });
        });
    });

window.WDS_Chosen_Multiple_Dropdown = {};
(function(window, $, that) {
    that.init = function() {
        that.cache();

        if (that.meetsRequirements()) {
            that.bindEvents();
        }
    };

    that.cache = function() {
        that.$c = {
            window: $(window),
            theDropdown: $('.chosen-select'),
            enfermedadAdyacenteSelect: $('#enfermedad-adyacente')
        };
    };

    that.bindEvents = function() {
        that.$c.window.on('load', that.applyChosen);
    };

    that.meetsRequirements = function() {
        return that.$c.theDropdown.length && that.$c.enfermedadAdyacenteSelect.length;
    };

    that.applyChosen = function() {
        that.$c.theDropdown.chosen({
            inherit_select_classes: true,
            
        });
    };

    $(that.init);

    // Obtener las opciones de enfermedades adyacentes
    fetch('/enfermedades')
        .then(response => response.json())
        .then(data => {
            data.enfermedades.forEach(enfermedad => {
                const option = document.createElement('option');
                option.value = enfermedad;
                option.text = enfermedad;
                that.$c.enfermedadAdyacenteSelect.append(option);
            });

            that.$c.enfermedadAdyacenteSelect.trigger('chosen:updated');
        });
})(window, jQuery, window.WDS_Chosen_Multiple_Dropdown);
