import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CourseWatchlistComponent } from './components/course-watchlist/course-watchlist.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatFormFieldModule} from "@angular/material/form-field";
import {MatSelectModule} from "@angular/material/select";
import {MatSlideToggleModule} from "@angular/material/slide-toggle";
import {MatInputModule} from "@angular/material/input";
import {ReactiveFormsModule} from "@angular/forms";
import {MatCardModule} from "@angular/material/card";
import {HttpClientModule} from "@angular/common/http";
import {MatButtonModule} from "@angular/material/button";

@NgModule({
  declarations: [
    AppComponent,
    CourseWatchlistComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatSlideToggleModule,
    MatInputModule,
    ReactiveFormsModule,
    MatCardModule,
    HttpClientModule,
    MatButtonModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
