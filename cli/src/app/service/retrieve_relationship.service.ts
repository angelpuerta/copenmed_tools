import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Graphs } from '../models/graphs';
import { Observable } from 'rxjs';


@Injectable()
export class RetrieveRelationshipService {

relationshipUrl = `${environment.apiUrl}/relationships/`;

constructor(private http: HttpClient) { }

public getRelationships(entity:string): Observable<Graphs>{
    return this.http.get<Graphs>(`${this.relationshipUrl}${entity}`);
  }

}