import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment.development';
import { Errores, Tabla } from '../interfaces/report.interface';

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  private baseUrl: string = environment.baseUrl;

  constructor( private http: HttpClient ) { }

  getErrores(  ){
    const url: string = `${this.baseUrl}/errores`
    return this.http.get<Errores>(url)
  }

  getTablaSimbolos( ){
    const url: string =`${this.baseUrl}/simbolos`
    return this.http.get<Tabla>(url)
  }

  getAST(){
    const url: string =`${this.baseUrl}/graficar`
      return this.http.get<any>(url)
  }
}
