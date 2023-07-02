import { Component, Input } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CodeModel } from '@ngstack/code-editor';
import { CompilerService } from '../../services/compiler.service';


@Component({
  selector: 'app-compiler-page',
  templateUrl: './compiler-page.component.html',
  styles: [`
  `]
})
export class CompilerPageComponent {
  codeSalida: string = ''
  @Input()
  code = [
    `import { TranslateModule, TranslateService } from '@ngstack/translate';`,
    `import { CodeEditorModule } from '@ngstack/code-editor';`,
    `import * as fs from 'fs';`,
    '',
    `export class MyClass {`,
    `  constructor(translate: TranslateService) {`,
    '',
    '  }',
    `}`
  ].join('\n');

  dependencies: string[] = [
    '@types/node',
    '@ngstack/translate',
    '@ngstack/code-editor'
  ];


  theme = 'vs-dark';

  codeModelCompiler: CodeModel = {
    language: 'typescript',
    uri: 'main.ts',
    value: '',
    dependencies: ['@types/node', '@ngstack/translate', '@ngstack/code-editor']
  };

  options = {
    contextmenu: true,
    minimap: {
      enabled: true
    }
  };

  optionsResponse = {
    lineNumbers: false,
    contextmenu: false,
    minimap: {
      enabled: false
    },
  };

  codeModelReponse: CodeModel = {
    language: 'json',
    uri: 'main.json',
    value: '',
  };

  validarBoton(): boolean {
    if( this.codeModelCompiler.value !== '' ){
      return false;
    }
    return true;
  }

  traducir(){
    this.codeSalida = '';
    this.compilerService.analizarCodigo( this.codeModelCompiler.value ).subscribe((res)=> {
      this.showSnackbar('Códio compilado correctamente')
      this.codeSalida = res
    })
  }

  constructor( private snackbar: MatSnackBar, private compilerService: CompilerService ) { }

  showSnackbar( message: string ): void{
    this.snackbar.open( message, 'ok', {
      duration: 3500
    })
  }
}
