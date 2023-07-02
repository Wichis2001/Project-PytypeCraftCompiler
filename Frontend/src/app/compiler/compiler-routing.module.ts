import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LayoutPageComponent } from './pages/layout-page/layout-page.component';
import { CompilerPageComponent } from './pages/compiler-page/compiler-page.component';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { ReportPageComponent } from './pages/report-page/report-page.component';

const routes: Routes = [
  {
    path: '',
    component: LayoutPageComponent,
    children: [
      {
        path: 'home',
        component: HomePageComponent
      },
      {
        path: 'compiler',
        component: CompilerPageComponent
      },
      {
        path: 'reports',
        component: ReportPageComponent
      },
      {
        path: '**',
        redirectTo: 'home'
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class CompilerRoutingModule { }
