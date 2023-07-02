import { Component } from '@angular/core';
import { Errores } from '../../interfaces/report.interface';
import { ReportService } from '../../services/report.service';

@Component({
  selector: 'app-errores-report',
  templateUrl: './errores-report.component.html',
  styles: [
  ]
})
export class ErroresReportComponent {
  columnas: string[] = ['No.', 'Detalle del Error'];
  errores: Errores = {
    valores: []
  }

  constructor( private reporteService: ReportService) {}

  ngOnInit(): void {
    this.reporteService.getErrores().subscribe( res => {
      this.errores = res;
    })

  }
}
