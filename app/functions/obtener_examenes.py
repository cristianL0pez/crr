def obtener_examenes(tipo_asa, tipo_riesgo):
    examenes = []

    if tipo_asa:
        asa_mayor = tipo_asa[0][1]

        if asa_mayor == "ASA 1":
            if tipo_riesgo == "Bajo Riesgo":
                examenes.append("No de rutina")
            elif tipo_riesgo == "Riesgo Medio":
                examenes.append("No de rutina")
            elif tipo_riesgo == "Alto Riesgo":
                examenes.append("Hemograma - Coagulación - ECG")
        elif asa_mayor == "ASA 2":
            if tipo_riesgo == "Bajo Riesgo":
                examenes.append("No de rutina")
            elif tipo_riesgo == "Riesgo Medio":
                examenes.append("Función renal - ECG")
            elif tipo_riesgo == "Alto Riesgo":
                examenes.append("Hemograma - Coagulación - Función renal - ECG")
        elif asa_mayor == "ASA 3":
            if tipo_riesgo == "Bajo Riesgo":
                examenes.append("Hemograma - Coagulación - ECG")
            elif tipo_riesgo == "Riesgo Medio":
                examenes.append("Hemograma - Coagulación - Función renal - ECG")
            elif tipo_riesgo == "Alto Riesgo":
                examenes.append("Hemograma - Coagulación - Función renal - ECG")
        elif asa_mayor == "ASA 4":
            if tipo_riesgo == "Bajo Riesgo":
                examenes.append("Hemograma - Coagulación - ECG - Función renal")
            elif tipo_riesgo == "Riesgo Medio":
                examenes.append("Hemograma - Coagulación - ECG - Función renal")
            elif tipo_riesgo == "Alto Riesgo":
                examenes.append("Hemograma - Coagulación - ECG - Función renal")

    return examenes

