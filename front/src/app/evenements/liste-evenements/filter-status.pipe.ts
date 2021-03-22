import { Pipe, PipeTransform } from '@angular/core';
import { Evenement, EvenementStatus } from '../evenements.service';

@Pipe({
  name: 'filterStatus'
})
export class FilterStatusPipe implements PipeTransform {

  transform(events: Evenement[], activeFilter: EvenementStatus): unknown {
    return events.filter(event => event.status === activeFilter);
  }

}
