import { Component } from '@angular/core';

@Component({
  selector: 'app-layout-page',
  templateUrl: './layout-page.component.html',
  styles: [
  ]
})
export class LayoutPageComponent {

  public sidebarItems = [
    {
      label: 'Home',
      icon: 'home',
      url: './home'
    },
    {
      label: 'Compiler',
      icon: 'terminal',
      url: './compiler'
    },
    {
      label: 'Reports',
      icon: 'article',
      url: './reports'
    }
  ]
}
