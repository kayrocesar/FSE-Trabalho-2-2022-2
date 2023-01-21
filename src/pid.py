class PID:
    Kp = 30.0  # Ganho Proporcional
    Ki = 0.2  # Ganho Integral
    Kd = 400.0  # Ganho Derivativo
    T = 1.0   # Período de Amostragem (ms)
    error_tot = 0.0
    error_prev = 0.0
    reference=0.0
    sig_control_MAX = 100.0
    sig_control_MIN = -100.0
    sig_control = 0.0


    def pid_update_ref(self,reference_):
         self.reference =  reference_

    def pid_control(self, saida_medida):
        erro = self.reference - saida_medida
        self.error_tot += erro # Acumula o erro (Termo Integral)

        if self.error_tot >= self.sig_control_MAX:
            self.error_tot = self.sig_control_MAX
        elif self.error_tot <= self.sig_control_MIN:
            self.error_tot = self.sig_control_MIN
        
        delta_error = erro - self.error_prev # Diferença entre os erros (Termo Derivativo)
        self.sig_control = self.Kp * erro + (self.Ki * self.T) * self.error_tot + (self.Kd / self.T) * delta_error # PID calcula sinal de controle

        if self.sig_control >= self.sig_control_MAX:
            self.sig_control = self.sig_control_MAX
        elif self.sig_control <= self.sig_control_MIN:
            self.sig_control = self.sig_control_MIN
        
        self.error_prev = erro
        print("Sig control decimal: ",self.sig_control)
        return self.sig_control
