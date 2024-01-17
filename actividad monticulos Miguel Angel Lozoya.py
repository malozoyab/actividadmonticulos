import heapq
import random
      
class Paciente:                                                
    def __init__(self, nombre, nivel_urgencia, horas_espera):
        self.nombre = nombre
        self.nivel_urgencia = nivel_urgencia
        self.horas_espera = horas_espera

    def __lt__(self, other):
        return self.nivel_urgencia > other.nivel_urgencia

    def __le__(self, other):
        return self.nivel_urgencia >= other.nivel_urgencia

    def __gt__(self, other):
        return self.horas_espera > other.horas_espera

    def __ge__(self, other):
        return self.horas_espera >= other.horas_espera

class SalaEmergencias:
    def __init__(self):
        self.max_heap = []              # Montículo máximo para urgencia
        self.min_heap = []              # Montículo mínimo para tiempo de espera
        self.tiempo_real = 0            # Contador para el tiempo de atencion de cada paciente
        self.total_horas_atencion= 0    # Contador total para el tiempo de atencion de todos los pacientes

    def agregar_paciente(self, paciente):       
        heapq.heappush(self.max_heap, paciente) #Agregar a Monticulo maximo
        heapq.heappush(self.min_heap, (-paciente.horas_espera, paciente)) #Agregar a Monticulo minimo

    def atender_pacientes(self, num_pacientes):
        pacientes_atendidos = []
        for i in range(num_pacientes):
            # Atender pacientes con urgencia máxima (nivel 10)
            if -self.max_heap[0].nivel_urgencia == -10:
                paciente_atendido = heapq.heappop(self.max_heap)
                self.min_heap.remove((-paciente_atendido.horas_espera, paciente_atendido))
                paciente_atendido.horas_espera_real = self.tiempo_real
                pacientes_atendidos.append(paciente_atendido)

            # Si no hay pacientes con urgencia máxima, pero hay pacientes que han esperado más de 5 horas, atenderlos
            elif -self.min_heap[0][0] >= 5:
                paciente_atendido = heapq.heappop(self.min_heap)[1]
                self.max_heap.remove(paciente_atendido)
                paciente_atendido.horas_espera_real = self.tiempo_real
                pacientes_atendidos.append(paciente_atendido)
                self.tiempo_real += 1

            # Si no hay pacientes con urgencia máxima ni espera de más de 5 horas, atender al de mayor urgencia
            else:
                paciente_atendido = heapq.heappop(self.max_heap)
                paciente_atendido.horas_espera_real = self.tiempo_real
                pacientes_atendidos.append(paciente_atendido)

            self.tiempo_real += 1
            self.total_horas_atencion += 1

        return pacientes_atendidos


sala_emergencias = SalaEmergencias()
pacientes = []

for i in range(20):
    nombre = f"Paciente {i + 1}"
    nivel_urgencia = random.randint(1, 10)
    horas_espera = random.randint(0, 10)
    paciente = Paciente(nombre, nivel_urgencia, horas_espera)
    sala_emergencias.agregar_paciente(paciente)
    pacientes.append(paciente)

pacientes_atendidos = sala_emergencias.atender_pacientes(len(pacientes))

# Generar reportes
print("reporte llegadas:")
for i, paciente in enumerate(pacientes):
    print(f"{i + 1}. {paciente.nombre} - Urgencia: {paciente.nivel_urgencia}, Tiempo de espera: {paciente.horas_espera} horas")

print("Reporte de Atención:")
for i, paciente in enumerate(pacientes_atendidos):
    print(f"{i + 1}. {paciente.nombre} - Urgencia: {paciente.nivel_urgencia}, Tiempo de espera real: {paciente.horas_espera_real} horas")

print(f"\nTotal de horas de atención: {sala_emergencias.total_horas_atencion} horas")