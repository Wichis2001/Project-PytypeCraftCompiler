import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { CodeEditorModule } from '@ngstack/code-editor';

import { CompilerPageComponent } from './pages/compiler-page/compiler-page.component';
import { CompilerRoutingModule } from './compiler-routing.module';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { LayoutPageComponent } from './pages/layout-page/layout-page.component';
import { MaterialModule } from '../shared/material/material.module';
import { ReportPageComponent } from './pages/report-page/report-page.component';
import { TablaSimbolosReportComponent } from './components/tabla-simbolos-report/tabla-simbolos-report.component';
import { ErroresReportComponent } from './components/errores-report/errores-report.component';





@NgModule({
  declarations: [
    LayoutPageComponent,
    CompilerPageComponent,
    HomePageComponent,
    ReportPageComponent,
    TablaSimbolosReportComponent,
    ErroresReportComponent
  ],
  imports: [
    CommonModule,
    CompilerRoutingModule,
    CodeEditorModule.forChild(),
    MaterialModule,
    ReactiveFormsModule,
    FormsModule
  ]
})
export class CompilerModule { }
