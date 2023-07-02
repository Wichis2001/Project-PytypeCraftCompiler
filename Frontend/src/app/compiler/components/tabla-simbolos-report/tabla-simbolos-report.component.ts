import { Component } from '@angular/core';
import { Tabla } from '../../interfaces/report.interface';
import { ReportService } from '../../services/report.service';

@Component({
  selector: 'app-tabla-simbolos-report',
  templateUrl: './tabla-simbolos-report.component.html',
  styles: [
  ]
})
export class TablaSimbolosReportComponent {
  columnas: string[] = ['No.', 'Nombre Variable', 'Valor', 'Tipo', 'Instancia', 'Fila', 'Columna'];
  errores: Tabla = {
    valores: []
  }

  constructor( private reporteService: ReportService) {}

  ngOnInit(): void {
    this.reporteService.getTablaSimbolos().subscribe( res => {
      this.errores = res;
    })

  }
}
