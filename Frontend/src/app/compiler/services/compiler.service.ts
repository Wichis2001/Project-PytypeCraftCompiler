import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { map } from 'rxjs';
import { environment } from 'src/environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class CompilerService {

  constructor( private http: HttpClient ) { }
  private baseUrl: string = environment.baseUrl;
  

  analizarCodigo( codigo:string ){
    const url: string = `${this.baseUrl}/prueba`
    return this.http.post<any>(url,{
      codigo
    }).pipe(map( data => data ))
  }
}
