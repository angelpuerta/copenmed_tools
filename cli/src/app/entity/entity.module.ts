import { NgModule } from '@angular/core';
import { RetrieveRelationshipService } from '../service/retrieve_relationship.service';
import { Entity } from './entity.component';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { CauseList } from './cause-list/cause-list.component';
import { CauseComponent } from './cause/cause.component';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatExpansionModule } from '@angular/material/expansion';
import { ExplainCause } from './cause/detailed_cause/explain_cause.component';
import { MatBadgeModule } from '@angular/material/badge';
import { MatButtonModule } from '@angular/material/button';
import  {MatTableModule } from '@angular/material/table';




@NgModule({
  declarations: [
    Entity, CauseList, CauseComponent, ExplainCause
  ],
  imports: [CommonModule, MatToolbarModule, MatListModule, MatIconModule, MatExpansionModule, MatBadgeModule, MatButtonModule, MatTableModule],
  providers: [RetrieveRelationshipService]
})
export class EntityModule { }