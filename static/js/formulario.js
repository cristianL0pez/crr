// Obtener las opciones de tipo de cirugía solo una vez
fetch('/tipos_cirugia')
    .then(response => response.json())
    .then(data => {
        const tipoCirugiaSelect = document.getElementById('tipo-cirugia-list');
        const existingOptions = Array.from(tipoCirugiaSelect.options).map(option => option.value);

        data.tipos_cirugia.forEach(tipoCirugia => {
            if (!existingOptions.includes(tipoCirugia)) {
                const option = document.createElement('option');
                option.value = tipoCirugia;
                tipoCirugiaSelect.appendChild(option);
            }
        });

        // Configurar Autocomplete para el campo "Tipo de Cirugía" si no se ha configurado previamente
        const inputFields = $('input[data-list]').not('.ui-autocomplete-input');
        inputFields.each(function () {
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

// Obtener las opciones de enfermedades adyacentes
fetch('/enfermedades')
    .then(response => response.json())
    .then(data => {
        const enfermedades = data.enfermedades;

        // Agregar las opciones al select utilizando Chosen
        const selectEnfermedad = jQuery("#enfermedad-adyacente");
        enfermedades.forEach(enfermedad => {
            selectEnfermedad.append(new Option(enfermedad, enfermedad));
        });

        // Inicializar Chosen en el campo select
        selectEnfermedad.chosen({
            placeholder_text_multiple: "Enfermedades"
        });

    });