import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {CourseWatchlistComponent} from "./components/course-watchlist/course-watchlist.component";

const routes: Routes = [
  {path: 'course/watchlist', component: CourseWatchlistComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
