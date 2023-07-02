import { Component } from '@angular/core';
import { ReportService } from '../../services/report.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-report-page',
  templateUrl: './report-page.component.html',
  styles: [
  ]
})
export class ReportPageComponent {
  error:boolean = false
  simbolos:boolean = false

  constructor( private reportService: ReportService,
               private router: Router ){}
  habilitarError(){
    this.error = true;
    this.simbolos = false
  }

  habilitarTabla(){
    this.error=false;
    this.simbolos = true
  }

  arbolParser(){
    this.reportService.getAST().subscribe( res => {
      window.location.href = 'http://localhost:5000/static/ast.gv.pdf';
    })
  }
}
