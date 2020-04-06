import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CookieService } from 'ngx-cookie-service';

import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HttpClient } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RouterModule, Routes} from '@angular/router';
import { GraphComponent } from './graph/graph.component';
import { GraphFormComponent } from './graph/graph-form/graph-form.component';
import { GraphWebglComponent } from './graph/graph-webgl/graph-webgl.component';

const appRoutes: Routes = [
  {path: '',
   component: LoginComponent},
  {path: 'graph',
   component: GraphComponent},
];

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    GraphComponent,
    GraphFormComponent,
    GraphWebglComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    HttpClientModule,
    AppRoutingModule,
    ReactiveFormsModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [ CookieService],
  bootstrap: [AppComponent]
})
export class AppModule { }
