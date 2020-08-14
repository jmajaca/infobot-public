import { Injectable } from '@angular/core';
import {Course} from "../../models/course";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class CourseService {

  courseUrl = environment.backendUrl + '/course';

  constructor(private httpClient: HttpClient) { }

  getAllCourses(): Observable<Course[]> {
    return this.httpClient.get<Course[]>(this.courseUrl);
  }

  saveCourse(course: Course): Observable<Course> {
    return this.httpClient.post<Course>(this.courseUrl, course);
  }

}
